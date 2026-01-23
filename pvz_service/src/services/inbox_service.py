from datetime import datetime, timedelta
from typing import Any, Awaitable, Callable, TypeVar

from src.dao.inboxDAO import InboxEventsDAO
from src.enums.inbox import EventStatus, EventType
from src.models.inbox.inbox import InboxEvents
from src.utils.exception_mapper import exception_map
from src.utils.exceptions import AppException, ClientException, InboxConflictException

T = TypeVar("T")


class InboxService:
    STALE_TIMEOUT = timedelta(seconds=30)

    def __init__(self, inbox_repo: InboxEventsDAO):
        self.inbox_repo = inbox_repo

    async def execute(
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

        inbox_event, is_created = await self.inbox_repo.create_idempotency_key(
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
        session = self.inbox_repo.session

        try:
            result = await handler()

            # Сериализуем результат (если это Pydantic модель -> dict)
            response_data = result.model_dump(mode="json") if hasattr(result, "model_dump") else result

            await self.inbox_repo.mark_completed(event_id, response_body=response_data)
            await session.commit()
            return result

        except AppException as e:
            await session.rollback()

            if e.is_client_error:
                await self.inbox_repo.mark_completed(event_id, response_body=e.to_response())
            else:
                await self.inbox_repo.mark_failed(event_id, response_body=e.to_response())

            await session.commit()

            raise

        except Exception as e:
            await session.rollback()

            error_response = {
                "status_code": 500,
                "error": "internal_error",
                "detail": str(e),
                "exception_type": type(e).__name__,
            }

            await self.inbox_repo.mark_failed(event_id, response_body=error_response)
            await session.commit()
            raise

    async def _handle_existing_event(
        self,
        event: InboxEvents,
        handler: Callable[[], Awaitable[T]],
    ) -> T | dict[str, Any]:
        """Обработка существующего события в зависимости от статуса."""

        if event.status == EventStatus.COMPLETED:
            # TODO: Здесь можно добавить лог "Return cached response for {event.event_id}"
            return self._return_cached_response(event.response_body)

        elif event.status == EventStatus.FAILED:
            await self.inbox_repo.reset_to_processing(event.event_id)
            return await self._process_new_event(event.event_id, handler)

        elif event.status == EventStatus.PROCESSING:
            return await self._handle_processing_state(event, handler)

        raise ValueError(f"Неизвестный статус: {event.status}")

    def _return_cached_response(self, response_body: dict[str, Any]) -> Any:
        """Возвращает кэш или пересоздает exception для 4xx."""
        if isinstance(response_body, dict) and "status_code" in response_body:
            status_code = response_body["status_code"]

            if 400 <= status_code < 500:
                raise self._recreate_exception(response_body)

        return response_body

    def _recreate_exception(self, error_data: dict[str, Any]) -> AppException:
        """Воссоздает exception из сохраненных данных."""

        error_code = error_data.get("error", "internal_error")
        detail = error_data.get("detail", "")

        exception_class = exception_map.get(error_code, ClientException)
        return exception_class(detail)

    async def _handle_processing_state(self, event: InboxEvents, handler: Callable[[], Awaitable[T]]) -> T:
        """Разруливание состояния PROCESSING (Fresh vs Stale)."""

        now = datetime.now(event.created_at.tzinfo)
        age = now - event.created_at

        if age < self.STALE_TIMEOUT:
            raise InboxConflictException(f"Операция {event.event_id} в процессе.")

        is_claimed = await self.inbox_repo.claim_stale_event(
            event_id=event.event_id,
            stale_threshold=now - self.STALE_TIMEOUT,
        )

        if is_claimed:
            return await self._process_new_event(event.event_id, handler)
        else:
            raise InboxConflictException("Операция, восстановленна другим работником")
