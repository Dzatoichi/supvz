package com.supvz.requests_service.model.dto;

import com.supvz.requests_service.model.entity.enums.AssignmentAction;

import java.time.LocalDateTime;

/**
 * ДТО-рекорд ответа мастера на запрос.
 */
public record RequestAssignmentDto(
        long id,
        long requestId,
        long handymanId,
        AssignmentAction action,
        LocalDateTime processedAt,
        LocalDateTime createdAt,
        LocalDateTime updatedAt,
        String comment
) {
}
