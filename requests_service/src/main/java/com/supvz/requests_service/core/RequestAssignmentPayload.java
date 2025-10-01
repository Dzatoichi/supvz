package com.supvz.requests_service.core;

import jakarta.validation.constraints.NotNull;

import java.util.UUID;

public record RequestAssignmentPayload(
        @NotNull UUID handymanId,
        String description
        ) {
}
