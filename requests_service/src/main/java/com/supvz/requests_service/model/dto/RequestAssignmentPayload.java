package com.supvz.requests_service.model.dto;

import com.supvz.requests_service.core.annotation.NullOrNotBlank;
import jakarta.validation.constraints.NotNull;

import java.util.UUID;

/**
* Схема для создания ответа на запрос.
 */
public record RequestAssignmentPayload(
        @NotNull long requestId,
        @NotNull long handymanId,
        @NullOrNotBlank
        String comment
        ) {
}
