package com.supvz.requests_service.core;


import java.util.UUID;

public record RequestAssignmentUpdatePayload(
        UUID handymanId,
        String description,
        Status status
) {
}
