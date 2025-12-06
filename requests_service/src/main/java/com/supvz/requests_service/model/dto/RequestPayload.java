package com.supvz.requests_service.model.dto;

import jakarta.validation.constraints.NotNull;

import java.util.UUID;

/**
 * Схема для создания заявки.
 */
public record RequestPayload(
        @NotNull int pvzId,
        @NotNull long appellantId,
        String description
) {
}
