from datetime import datetime
from typing import Any, Tuple

from sqlalchemy import func, select, update
from sqlalchemy.dialects.postgresql import insert
from sqlalchemy.ext.asyncio import AsyncSession

from src.dao.baseDAO import BaseDAO
from src.enums.inbox import EventStatus, EventType
from src.models.inbox.inbox import InboxEvents
from src.utils.exceptions import DatabaseException


class InboxEventsDAO(BaseDAO[InboxEvents]):
    """
    Класс, наследующий базовый DAO для работы c сущностью InboxEvents.
    """

    def __init__(self, session: AsyncSession):
        super().__init__(model=InboxEvents, session=session)

    async def get_by_event_id(
        self,
        event_id: str,
    ) -> InboxEvents | None:
        """Получить событие по ID."""
        query = select(self.model).where(self.model.event_id == event_id)
        result = await self.session.execute(query)
        return result.scalar_one_or_none()

    async def create_event(
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
        stmt = (
            insert(self.model)
            .values(
                event_id=event_id,
                event_type=event_type,
                payload=payload,
                status=EventStatus.PROCESSING,
            )
            .on_conflict_do_nothing(index_elements=["event_id"])
            .returning(self.model)
        )

        result = await self.session.execute(stmt)
        new_event = result.scalar_one_or_none()

        if new_event:
            await self.session.commit()
            return new_event, True

        existing_event = await self.get_by_event_id(event_id)

        if not existing_event:
            await self.session.rollback()
            raise DatabaseException(f"Race condition обнаружена для event_id={event_id}")

        return existing_event, False

    async def mark_completed(
        self,
        event_id: str,
        response_body: dict[str, Any] | None,
    ) -> InboxEvents:
        """Обновляет статус на COMPLETED и сохраняет ответ."""
        stmt = (
            update(self.model)
            .where(self.model.event_id == event_id)
            .values(status=EventStatus.COMPLETED, response_body=response_body, finished_at=func.now())
            .returning(self.model)
        )
        result = await self.session.execute(stmt)
        return result.scalar_one()

    async def mark_failed(
        self,
        event_id: str,
        response_body: dict,
    ) -> InboxEvents:
        """Обновляет статус на FAILED и сохраняет ошибку."""
        stmt = (
            update(self.model)
            .where(self.model.event_id == event_id)
            .values(status=EventStatus.FAILED, response_body=response_body, finished_at=func.now())
            .returning(self.model)
        )
        result = await self.session.execute(stmt)
        return result.scalar_one()

    async def reset_to_processing(self, event_id: str) -> InboxEvents:
        """Сбрасывает статус на PROCESSING (для повторной попытки после FAILED)."""
        stmt = (
            update(self.model)
            .where(self.model.event_id == event_id)
            .values(
                status=EventStatus.PROCESSING,
                finished_at=None,
                created_at=func.now(),
            )
            .returning(self.model)
        )
        result = await self.session.execute(stmt)
        await self.session.commit()
        return result.scalar_one()

    async def claim_stale_event(
        self,
        event_id: str,
        stale_threshold: datetime,
    ) -> bool:
        """
        Атомарно пытается захватить зависшее (stale) событие.

        SQL: UPDATE inbox SET created_at=NOW()
             WHERE event_id=X AND status='processing' AND created_at < threshold

        Возвращает True, если удалось захватить.
        """
        stmt = (
            update(self.model)
            .where(
                self.model.event_id == event_id,
                self.model.status == EventStatus.PROCESSING,
                self.model.created_at < stale_threshold,
            )
            .values(created_at=func.now())
            .returning(self.model.event_id)
        )

        result = await self.session.execute(stmt)
        success = result.scalar_one_or_none() is not None

        if success:
            await self.session.commit()
        return success
