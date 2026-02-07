from datetime import datetime

from fastapi_pagination import Page, Params
from fastapi_pagination.ext.sqlalchemy import paginate
from sqlalchemy import select, update
from sqlalchemy.ext.asyncio import AsyncSession

from src.dao.baseDAO import BaseDAO
from src.models.salary_rules import SalaryRule
from src.schemas.salary_schemas import (
    SalaryRuleCreateSchema,
    SalaryRuleFilterSchema,
    SalaryRuleReadSchema,
    SalaryRuleUpdateSchema,
)


class SalaryRuleDAO(BaseDAO[SalaryRule]):
    """DAO для работы с правилами расчета зарплаты."""

    def __init__(self, session: AsyncSession):
        """Инициализация SalaryRuleDAO."""
        super().__init__(session=session, model=SalaryRule)

    @BaseDAO.with_exception
    async def create_rule(self, data: SalaryRuleCreateSchema) -> SalaryRuleReadSchema:
        """Создание нового правила расчета зарплаты."""
        obj = await super().create(data)
        return SalaryRuleReadSchema.model_validate(obj)

    @BaseDAO.with_exception
    async def get_rule_by_id(self, rule_id: int) -> SalaryRuleReadSchema | None:
        """Получение правила по ID."""
        obj = await super().get_by_id(rule_id)
        if obj:
            return SalaryRuleReadSchema.model_validate(obj)
        return None

    @BaseDAO.with_exception
    async def get_rules(self, *args, **kwargs) -> list[SalaryRuleReadSchema]:
        """Получение правил по любым фильтрам."""
        stmt = select(self.model)
        if args:
            stmt = stmt.filter(*args)
        if kwargs:
            stmt = stmt.filter_by(**kwargs)
        result = await self.session.execute(stmt)
        return [SalaryRuleReadSchema.model_validate(obj) for obj in result.scalars().all()]

    @BaseDAO.with_exception
    async def get_rule(self, *args, **kwargs) -> SalaryRuleReadSchema | None:
        """Получение одного правила по любым фильтрам."""
        stmt = select(self.model)
        if args:
            stmt = stmt.filter(*args)
        if kwargs:
            stmt = stmt.filter_by(**kwargs)
        result = await self.session.execute(stmt)
        obj = result.scalar_one_or_none()
        if obj:
            return SalaryRuleReadSchema.model_validate(obj)
        return None

    @BaseDAO.with_exception
    async def get_rules_paginated(
        self,
        params: Params,
        filters: SalaryRuleFilterSchema | None = None,
    ) -> Page[SalaryRuleReadSchema]:
        """Получение списка правил с пагинацией и фильтрацией."""
        stmt = select(self.model)

        if filters:
            if filters.pvz_id is not None:
                stmt = stmt.where(self.model.pvz_id == filters.pvz_id)
            if filters.rule_type is not None:
                stmt = stmt.where(self.model.rule_type == filters.rule_type)
            if filters.is_active is not None:
                stmt = stmt.where(self.model.is_active == filters.is_active)

        stmt = stmt.order_by(self.model.id.desc())

        page = await paginate(self.session, stmt, params)
        return Page(
            items=[SalaryRuleReadSchema.model_validate(item) for item in page.items],
            total=page.total,
            page=page.page,
            pages=page.pages,
            size=page.size,
        )

    @BaseDAO.with_exception
    async def update_rule(self, rule_id: int, data: SalaryRuleUpdateSchema) -> SalaryRuleReadSchema | None:
        """Обновление правила расчета зарплаты."""
        update_data = data.model_dump(exclude_unset=True, exclude_none=True)
        if not update_data:
            return await self.get_rule_by_id(rule_id)
        update_data["updated_at"] = datetime.now()
        stmt = update(self.model).where(self.model.id == rule_id).values(**update_data).returning(self.model)
        result = await self.session.execute(stmt)
        await self.session.commit()
        obj = result.scalar_one_or_none()
        if obj:
            await self.session.refresh(obj)
            return SalaryRuleReadSchema.model_validate(obj)
        return None

    @BaseDAO.with_exception
    async def delete_rule(self, rule_id: int) -> bool:
        """Удаление правила расчета зарплаты."""
        await super().delete(rule_id)

    @BaseDAO.with_exception
    async def deactivate_rule(self, rule_id: int) -> bool:
        """Мягкое удаление правила (деактивация)."""
        stmt = update(self.model).where(self.model.id == rule_id).values(is_active=False, updated_at=datetime.now())
        result = await self.session.execute(stmt)
        await self.session.commit()
        return result.rowcount > 0

    @BaseDAO.with_exception
    async def exists_for_pvz(self, pvz_id: int) -> bool:
        """Проверка существования правила для ПВЗ."""
        stmt = select(self.model.id).where(self.model.pvz_id == pvz_id)
        result = await self.session.execute(stmt)
        return result.scalar_one_or_none() is not None
