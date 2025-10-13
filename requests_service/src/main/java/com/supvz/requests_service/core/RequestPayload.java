package com.supvz.requests_service.core;

import jakarta.validation.constraints.NotNull;

import java.util.UUID;

/*
Схема (Payload) для создания запроса мастеру.
 */
public record RequestPayload (
        @NotNull Integer pvzId,
        @NotNull UUID appellantId,
        String description
) {
}
