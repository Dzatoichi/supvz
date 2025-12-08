package com.supvz.requests_service.model.dto;

import com.supvz.requests_service.core.enums.AssignmentAction;
import com.supvz.requests_service.core.enums.RequestStatus;
import lombok.Builder;

import java.time.LocalDateTime;
import java.util.UUID;

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
