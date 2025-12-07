package com.supvz.requests_service.model.dto;

import com.supvz.requests_service.core.enums.RequestStatus;

public record RequestPlainDto(
        long id,
        int pvzId,
        long appellantId,
        RequestStatus status,
        String subject,
        String description
) {
}
