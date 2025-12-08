package com.supvz.requests_service.model.dto;

import com.supvz.requests_service.core.annotation.NullOrNotBlank;
import com.supvz.requests_service.core.annotation.EmptyOrSize;
import jakarta.validation.constraints.NotNull;

/**
 * Схема для создания заявки.
 */
public record RequestPayload(
        @NotNull int pvzId,
        @NotNull long appellantId,
        @EmptyOrSize(min = 5, max = 64)
        @NullOrNotBlank
        String subject,
        @NullOrNotBlank
        String description
) {
}