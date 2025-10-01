package com.supvz.requests_service.core;

import jakarta.validation.constraints.NotNull;

import java.util.UUID;

public record RequestPayload (
        @NotNull int pvzId,
        @NotNull UUID appellantId,
        String description
) {
}
