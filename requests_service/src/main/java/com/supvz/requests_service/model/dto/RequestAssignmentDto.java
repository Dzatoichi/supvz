package com.supvz.requests_service.model.dto;

import com.supvz.requests_service.core.enums.Status;
import lombok.Builder;

import java.time.LocalDateTime;
import java.util.UUID;

@Builder
/*
ДТО ответа мастера для запроса.
 */
public record RequestAssignmentDto(
        long id,
        long requestId,
        UUID handymanId,
        Status status,
        LocalDateTime assignedAt,
        LocalDateTime completedAt,
        String description
) {
}
