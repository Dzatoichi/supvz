from fastapi_pagination import Page, Params

from src.dao.salary_rulesDAO import SalaryRuleDAO
from src.schemas.salary_schemas import (
    SalaryRuleCreateSchema,
    SalaryRuleFilterSchema,
    SalaryRuleReadSchema,
    SalaryRuleUpdateSchema,
)
from src.utils.exceptions import SalaryRuleNotFoundException


class SalaryRulesService:
    """Сервис для бизнес-логики работы с правилами расчета зарплаты."""

    def __init__(self, dao: SalaryRuleDAO):
        """Инициализация сервиса."""
        self.dao = dao

    async def create_rule(self, data: SalaryRuleCreateSchema) -> SalaryRuleReadSchema:
        """Создание правила расчета зарплаты."""
        return await self.dao.create_rule(data)

    async def get_rule_by_id(self, rule_id: int) -> SalaryRuleReadSchema:
        """Получение правила по ID."""
        rule = await self.dao.get_rule_by_id(rule_id)
        if not rule:
            raise SalaryRuleNotFoundException()
        return rule

    async def get_rules(
        self,
        params: Params,
        filters: SalaryRuleFilterSchema | None = None,
    ) -> Page[SalaryRuleReadSchema]:
        """Получение списка правил с фильтрацией."""
        return await self.dao.get_rules_paginated(params=params, filters=filters)

    async def update_rule(
        self,
        rule_id: int,
        data: SalaryRuleUpdateSchema,
    ) -> SalaryRuleReadSchema:
        """Обновление правила расчета зарплаты."""
        existing = await self.dao.get_rule_by_id(rule_id)
        if not existing:
            raise SalaryRuleNotFoundException()
        updated = await self.dao.update_rule(rule_id, data)
        if not updated:
            raise SalaryRuleNotFoundException()
        return updated

    async def delete_rule(self, rule_id: int) -> None:
        """Удаление правила расчета зарплаты."""
        existing = await self.dao.get_rule_by_id(rule_id)
        if not existing:
            raise SalaryRuleNotFoundException()
        await self.dao.delete_rule(rule_id)

    async def deactivate_rule(self, rule_id: int) -> bool:
        """Мягкое удаление правила (деактивация)."""
        existing = await self.dao.get_rule_by_id(rule_id)
        if not existing:
            raise SalaryRuleNotFoundException()
        return await self.dao.deactivate_rule(rule_id)
