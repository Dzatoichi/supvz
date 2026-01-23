from datetime import datetime, timedelta
from typing import Any, Awaitable, Callable, TypeVar

from src.dao.inboxDAO import InboxEventsDAO
from src.enums.inbox import EventStatus, EventType
from src.models.inbox.inbox import InboxEvents
from src.utils.exceptions import InboxConflictException

T = TypeVar("T")


class InboxService:
    STALE_TIMEOUT = timedelta(seconds=30)

    def __init__(self, db_helper, dao: InboxEventsDAO):
        self.dao = dao
        self.db_helper = db_helper

    async def execute_idempotent(
        self,
        event_id: str,
        event_type: EventType,
        payload: dict[str, Any],
        handler: Callable[[], Awaitable[T]],
    ) -> T | dict[str, Any]:
        """
        Главный метод идемпотентности.

        Args:
            event_id: Уникальный ID запроса
            event_type: Тип операции
            payload: Данные запроса
            handler: Асинхронная функция с бизнес-логикой, которую надо выполнить

        Returns:
            Результат выполнения handler или кешированный ответ.
        """

        inbox_event, is_created = await self.dao.create_idempotency_key(
            event_id=event_id,
            event_type=event_type,
            payload=payload,
        )

        if is_created:
            return await self._process_new_event(inbox_event.event_id, handler)

        # Запись уже существует - разбираем статусы
        return await self._handle_existing_event(inbox_event, handler)

    async def _process_new_event(self, event_id: str, handler: Callable[[], Awaitable[T]]) -> T:
        """Выполнение логики для нового события."""
        async with self.db_helper.async_session_maker() as session:
            try:
                result = await handler()

                # Сериализуем результат (если это Pydantic модель -> dict)
                response_data = result.model_dump() if hasattr(result, "model_dump") else result

                await self.dao.mark_completed(event_id, response_body=response_data, session=session)
                await session.commit()
                return result

            except Exception as e:
                await session.rollback()
                await self.dao.mark_failed(event_id, error_info=str(e), session=session)
                await session.commit()
            raise e

    async def _handle_existing_event(
        self,
        event: InboxEvents,
        handler: Callable[[], Awaitable[T]],
    ) -> T | dict[str, Any]:
        """Обработка существующего события в зависимости от статуса."""

        if event.status == EventStatus.COMPLETED:
            # TODO: Здесь можно добавить лог "Return cached response for {event.event_id}"
            return event.response_body

        if event.status == EventStatus.FAILED:
            async with self.db_helper.async_session_maker() as session:
                await self.dao.reset_to_processing(event.event_id, session=session)
                return await self._process_new_event(event.event_id, handler)

        if event.status == EventStatus.PROCESSING:
            return await self._handle_processing_state(event, handler)

        raise ValueError(f"Неизвестный статус: {event.status}")

    async def _handle_processing_state(self, event: InboxEvents, handler: Callable[[], Awaitable[T]]) -> T:
        """Разруливание состояния PROCESSING (Fresh vs Stale)."""

        # Вычисляем "возраст" записи.
        # created_at имеет timezone, поэтому используем now(utc)
        now = datetime.now(event.created_at.tzinfo)
        age = now - event.created_at

        # 1. Запись свежая (еще не истек таймаут) -> Реальный конфликт
        if age < self.STALE_TIMEOUT:
            retry_after = int((self.STALE_TIMEOUT - age).total_seconds())
            raise InboxConflictException(
                message=f"Operation {event.event_id} is in progress", retry_after=max(1, retry_after)
            )

        # 2. Запись протухла (Stale) -> Пытаемся захватить
        is_claimed = await self.dao.claim_stale_event(event_id=event.event_id, stale_threshold=now - self.STALE_TIMEOUT)

        if is_claimed:
            # Успешно захватили -> выполняем заново
            return await self._process_new_event(event.event_id, handler)
        else:
            # Не смогли захватить (race condition, кто-то успел быстрее) -> Конфликт
            raise InboxConflictException(message="Operation recovered by another worker", retry_after=5)
