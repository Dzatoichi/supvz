from fastapi import APIRouter, Depends, Query, status
from fastapi_pagination import Page, Params

from src.schemas.salary_schemas import (
    SalaryRuleCreateSchema,
    SalaryRuleFilterSchema,
    SalaryRuleReadSchema,
    SalaryRuleType,
    SalaryRuleUpdateSchema,
)
from src.services.salary_rules_service import SalaryRulesService
from src.utils.dependencies import get_salary_rule_service

salary_rules_router = APIRouter(prefix="/salary-rules", tags=["Salary Rules"])


@salary_rules_router.post(
    "",
    response_model=SalaryRuleReadSchema,
    status_code=status.HTTP_201_CREATED,
)
async def create_salary_rule(
    data: SalaryRuleCreateSchema,
    service: SalaryRulesService = Depends(get_salary_rule_service),
) -> SalaryRuleReadSchema:
    """Создать новое правило расчета зарплаты."""
    return await service.create_rule(data)


@salary_rules_router.get(
    "",
    response_model=Page[SalaryRuleReadSchema],
)
async def get_salary_rules(
    params: Params = Depends(),
    pvz_id: int | None = Query(None, description="ID пункта выдачи заказов"),
    rule_type: SalaryRuleType | None = Query(None, description="Тип правила расчета"),
    is_active: bool | None = Query(None, description="Активно ли правило"),
    service: SalaryRulesService = Depends(get_salary_rule_service),
) -> Page[SalaryRuleReadSchema]:
    """Получить список правил расчета зарплаты с фильтрацией и пагинацией."""
    filters = SalaryRuleFilterSchema(
        pvz_id=pvz_id,
        rule_type=rule_type,
        is_active=is_active,
    )
    return await service.get_rules(params=params, filters=filters)


@salary_rules_router.get(
    "/{rule_id}",
    response_model=SalaryRuleReadSchema,
)
async def get_salary_rule(
    rule_id: int,
    service: SalaryRulesService = Depends(get_salary_rule_service),
) -> SalaryRuleReadSchema:
    """Получить правило расчета зарплаты по ID."""
    return await service.get_rule_by_id(rule_id)


@salary_rules_router.patch(
    "/{rule_id}",
    response_model=SalaryRuleReadSchema,
)
async def update_salary_rule(
    rule_id: int,
    data: SalaryRuleUpdateSchema,
    service: SalaryRulesService = Depends(get_salary_rule_service),
) -> SalaryRuleReadSchema:
    """Обновить существующее правило расчета зарплаты."""
    return await service.update_rule(rule_id, data)


@salary_rules_router.delete(
    "/{rule_id}",
    status_code=status.HTTP_204_NO_CONTENT,
)
async def delete_salary_rule(
    rule_id: int,
    service: SalaryRulesService = Depends(get_salary_rule_service),
) -> None:
    """Удалить правило расчета зарплаты."""
    await service.delete_rule(rule_id)


@salary_rules_router.post(
    "/{rule_id}/deactivate",
    status_code=status.HTTP_204_NO_CONTENT,
)
async def deactivate_salary_rule(
    rule_id: int,
    service: SalaryRulesService = Depends(get_salary_rule_service),
) -> None:
    """Деактивировать правило расчета зарплаты."""
    await service.deactivate_rule(rule_id)
