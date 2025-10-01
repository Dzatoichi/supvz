package com.supvz.requests_service.core;

import lombok.Builder;

import java.util.List;
import java.util.UUID;

@Builder
public record RequestDto(
        long id,
        int pvzId,
        UUID appellantId,
        String description,
        List<RequestAssignmentDto> assignments
) {
}
