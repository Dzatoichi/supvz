package com.supvz.requests_service.model.dto;


import com.supvz.requests_service.core.annotation.NullOrNotBlank;
import com.supvz.requests_service.core.enums.AssignmentAction;

import java.util.UUID;

/**
 * Схема полезной нагрузки заявки для обновления.
 */
public record RequestAssignmentUpdatePayload(
        AssignmentAction action,
        Long handymanId,
        @NullOrNotBlank
        String comment
) {
}