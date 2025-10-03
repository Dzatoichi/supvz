package com.supvz.requests_service.core;


import jakarta.validation.constraints.NotNull;

import java.util.UUID;

public record RequestAssignmentUpdatePayload(
        @NotNull Status status,
        UUID handymanId,
        String description
) {
}
