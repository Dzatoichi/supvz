package com.supvz.requests_service.model.dto;

import lombok.Builder;

import java.util.List;
import java.util.UUID;

@Builder
/*
ДТО запроса мастеру.
 */
public record RequestDto(
        long id,
        int pvzId,
        UUID appellantId,
        String description,
        List<RequestAssignmentDto> assignments
) {
}
