from datetime import datetime
from typing import Any, Tuple

from sqlalchemy import func, insert, select, update
from sqlalchemy.ext.asyncio import AsyncSession

from src.dao.baseDAO import BaseDAO
from src.enums.inbox import EventStatus, EventType
from src.models.inbox.inbox import InboxEvents


class InboxEventsDAO(BaseDAO[InboxEvents]):
    """
    Класс, наследующий базовый DAO для работы c сущностью InboxEvents.
    """

    def __init__(self):
        super().__init__(model=InboxEvents)

    async def get_by_event_id(
        self,
        event_id: str,
        session: AsyncSession,
    ) -> InboxEvents | None:
        """Получить событие по ID."""
        query = select(InboxEvents).where(InboxEvents.event_id == event_id)
        result = await session.execute(query)
        return result.scalar_one_or_none()

    async def create_idempotency_key(
        self,
        event_id: str,
        event_type: EventType,
        payload: dict[str, Any],
    ) -> Tuple[InboxEvents, bool]:
        """
        Создает запись.

        Возвращает кортеж:
        (InboxEvents, is_created: bool)

        Если запись создана -> is_created=True
        Если запись уже была -> is_created=False, возвращаем существующую
        """
        async with self._get_session() as session:
            stmt = (
                insert(InboxEvents)
                .values(
                    event_id=event_id,
                    event_type=event_type,
                    payload=payload,
                    status=EventStatus.PROCESSING,
                )
                .on_conflict_do_nothing(index_elements=[InboxEvents.event_id])
                .returning(InboxEvents)
            )

            result = await session.execute(stmt)
            new_event = result.scalar_one_or_none()

            if new_event:
                return new_event, True

            existing_event = await self.get_by_event_id(event_id, session)

            if not existing_event:
                raise ValueError(f"Race condition обнаружена для event_id={event_id}")

            return existing_event, False

    async def mark_completed(self, event_id: str, response_body: dict[str, Any] | None) -> InboxEvents:
        """Обновляет статус на COMPLETED и сохраняет ответ."""
        async with self._get_session() as session:
            stmt = (
                update(InboxEvents)
                .where(InboxEvents.event_id == event_id)
                .values(status=EventStatus.COMPLETED, response_body=response_body, finished_at=func.now())
                .returning(InboxEvents)
            )
            result = await session.execute(stmt)
            return result.scalar_one()

    async def mark_failed(self, event_id: str, error_info: str) -> InboxEvents:
        """Обновляет статус на FAILED и сохраняет ошибку."""
        async with self._get_session() as session:
            stmt = (
                update(InboxEvents)
                .where(InboxEvents.event_id == event_id)
                .values(status=EventStatus.FAILED, error_info=error_info, finished_at=func.now())
                .returning(InboxEvents)
            )
            result = await session.execute(stmt)
            return result.scalar_one()

    async def reset_to_processing(self, event_id: str) -> InboxEvents:
        """Сбрасывает статус на PROCESSING (для повторной попытки после FAILED)."""
        async with self._get_session() as session:
            stmt = (
                update(InboxEvents)
                .where(InboxEvents.event_id == event_id)
                .values(
                    status=EventStatus.PROCESSING,
                    error_info=None,
                    finished_at=None,
                    created_at=func.now(),
                )
                .returning(InboxEvents)
            )
            result = await session.execute(stmt)
            return result.scalar_one()

    async def claim_stale_event(self, event_id: str, stale_threshold: datetime) -> bool:
        """
        Атомарно пытается захватить зависшее (stale) событие.

        SQL: UPDATE inbox SET created_at=NOW()
             WHERE event_id=X AND status='processing' AND created_at < threshold

        Возвращает True, если удалось захватить.
        """
        async with self._get_session() as session:
            stmt = (
                update(InboxEvents)
                .where(
                    InboxEvents.event_id == event_id,
                    InboxEvents.status == EventStatus.PROCESSING,
                    InboxEvents.created_at < stale_threshold,
                )
                .values(created_at=func.now())
                .returning(InboxEvents.event_id)
            )

            result = await session.execute(stmt)
            return result.scalar_one_or_none() is not None
