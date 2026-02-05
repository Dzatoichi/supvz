from datetime import date, datetime
from enum import Enum

from pydantic import BaseModel, ConfigDict, Field, field_validator, model_validator


class RequestTypeEnum(str, Enum):
    """Тип запроса на смену."""

    ADD = "add"
    CANCEL = "cancel"
    CHANGE = "change"


class RequestStatusEnum(str, Enum):
    """Статус запроса на смену."""

    PENDING = "pending"
    APPROVED = "approved"
    REJECTED = "rejected"
    CANCELLED_BY_USER = "cancelled_by_user"
    CANCELLED_BY_SYSTEM = "cancelled_by_system"


class ShiftRequestBaseSchema(BaseModel):
    """Базовая схема запроса на смену."""

    scheduled_shift_id: int = Field(
        default=None,
        description="ID запланированной смены",
    )
    user_id: int = Field(..., description="ID пользователя")
    request_type: RequestTypeEnum = Field(..., description="Тип запроса")
    new_user_id: int | None = Field(
        default=None,
        description="ID нового пользователя (для передачи смены)",
    )
    reason: str | None = Field(
        default=None,
        max_length=2000,
        description="Причина запроса",
    )
    scheduled_shift_start_time: datetime = Field(
        ...,
        description="Время начала запланированной смены",
    )

    model_config = ConfigDict(from_attributes=True)


class ShiftRequestCreateSchema(BaseModel):
    """Схема создания запроса на смену."""

    scheduled_shift_id: int = Field(
        default=None,
        description="ID запланированной смены (обязательно для cancel/change)",
    )
    user_id: int = Field(..., description="ID пользователя")
    request_type: RequestTypeEnum = Field(..., description="Тип запроса")
    new_user_id: int | None = Field(
        default=None,
        description="ID нового пользователя (обязательно для change)",
    )
    reason: str | None = Field(
        default=None,
        max_length=2000,
        description="Причина запроса",
    )
    scheduled_shift_start_time: datetime = Field(
        ...,
        description="Время начала запланированной смены",
    )

    @field_validator("scheduled_shift_start_time")
    @classmethod
    def validate_shift_start_time(cls, v: datetime) -> datetime:
        """Валидирует время начала смены."""
        if v is not None and v.tzinfo is not None:
            v = v.replace(tzinfo=None)

        if v is not None and v.date() < date.today():
            raise ValueError("Нельзя создать запрос на смену на прошедший день")

        return v

    @model_validator(mode="after")
    def validate_request_fields(self) -> "ShiftRequestCreateSchema":
        """Валидация полей в зависимости от типа запроса."""
        if self.request_type in (RequestTypeEnum.CANCEL, RequestTypeEnum.CHANGE):
            if self.scheduled_shift_id is None:
                raise ValueError("scheduled_shift_id обязателен для запросов типа cancel/change")

        if self.request_type == RequestTypeEnum.CHANGE:
            if self.new_user_id is None:
                raise ValueError("new_user_id обязателен для запросов типа change")

        return self


class ShiftRequestUpdateSchema(BaseModel):
    """Схема обновления запроса на смену."""

    reason: str | None = Field(
        default=None,
        max_length=2000,
        description="Причина запроса",
    )


class ShiftRequestProcessSchema(BaseModel):
    """Схема обработки запроса на смену (одобрение/отклонение)."""

    status: RequestStatusEnum = Field(
        ...,
        description="Новый статус запроса",
    )
    processed_by: int = Field(..., description="ID обработавшего пользователя")
    response: str | None = Field(
        default=None,
        max_length=2000,
        description="Ответ от обработавшего (комментарий к одобрению/отклонению)",
    )

    @field_validator("status")
    @classmethod
    def validate_status(cls, v: RequestStatusEnum) -> RequestStatusEnum:
        """Проверяет, что статус допустим для обработки."""
        allowed = (RequestStatusEnum.APPROVED, RequestStatusEnum.REJECTED)
        if v not in allowed:
            raise ValueError(f"Статус должен быть одним из: {', '.join(s.value for s in allowed)}")
        return v


class ShiftRequestReadSchema(BaseModel):
    """Схема чтения запроса на смену."""

    id: int
    scheduled_shift_id: int | None
    user_id: int
    request_type: RequestTypeEnum
    new_user_id: int | None
    status: RequestStatusEnum
    requested_at: datetime
    processed_at: datetime | None
    processed_by: int | None
    reason: str | None
    response: str | None
    scheduled_shift_start_time: datetime
    created_at: datetime
    updated_at: datetime

    model_config = ConfigDict(from_attributes=True)


class ShiftRequestFilterSchema(BaseModel):
    """Схема фильтрации запросов на смену."""

    user_id: int | None = Field(default=None, description="ID пользователя")
    scheduled_shift_id: int | None = Field(
        default=None,
        description="ID запланированной смены",
    )
    request_type: RequestTypeEnum | None = Field(
        default=None,
        description="Тип запроса",
    )
    status: RequestStatusEnum | None = Field(
        default=None,
        description="Статус запроса",
    )
    requested_at_from: datetime | None = Field(
        default=None,
        description="Дата запроса от",
    )
    requested_at_to: datetime | None = Field(
        default=None,
        description="Дата запроса до",
    )
    scheduled_shift_start_time_from: datetime | None = Field(
        default=None,
        description="Время начала смены от",
    )
    scheduled_shift_start_time_to: datetime | None = Field(
        default=None,
        description="Время начала смены до",
    )

    @field_validator(
        "requested_at_from",
        "requested_at_to",
        "scheduled_shift_start_time_from",
        "scheduled_shift_start_time_to",
    )
    @classmethod
    def remove_timezone(cls, v: datetime | None) -> datetime | None:
        """Удаляет информацию о часовом поясе из datetime."""
        if v is not None and v.tzinfo is not None:
            return v.replace(tzinfo=None)
        return v
