package com.supvz.requests_service.core;


import jakarta.validation.constraints.NotNull;

public record RequestUpdatePayload(
        @NotNull Integer pvzId,
        String description
) {
}
