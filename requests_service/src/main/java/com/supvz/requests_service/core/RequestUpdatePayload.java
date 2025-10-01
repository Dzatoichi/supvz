package com.supvz.requests_service.core;


public record RequestUpdatePayload(
        Integer pvzId,
        String description
) {
}
