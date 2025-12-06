package com.supvz.requests_service.model.dto;

import jakarta.validation.constraints.NotNull;

import java.util.UUID;

/**
* Схема для создания ответа на запрос.
 */
public record RequestAssignmentPayload(
        @NotNull long handymanId,
        String comment
        ) {
}
