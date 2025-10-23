package com.supvz.requests_service.core;

import jakarta.validation.constraints.NotNull;

import java.util.UUID;

/*
Схема (Payload) для создания ответа на запрос.
 */
public record RequestAssignmentPayload(
        @NotNull UUID handymanId,
        String description
        ) {
}
