package com.supvz.requests_service.model.dto;


import com.supvz.requests_service.core.enums.Status;
import jakarta.validation.constraints.NotNull;

import java.util.UUID;

/*
Схема (Payload) для обновления ответа на запрос.
 */
public record RequestAssignmentUpdatePayload(
        @NotNull Status status,
        UUID handymanId,
        String description
) {
}
