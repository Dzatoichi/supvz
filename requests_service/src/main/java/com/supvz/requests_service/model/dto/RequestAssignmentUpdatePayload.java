package com.supvz.requests_service.model.dto;


import com.supvz.requests_service.core.annotation.NullOrNotBlank;
import com.supvz.requests_service.core.annotation.NullOrNotSystemCancel;
import com.supvz.requests_service.model.entity.enums.AssignmentAction;

/**
 * Схема полезной нагрузки заявки для обновления.
 */
public record RequestAssignmentUpdatePayload(
        @NullOrNotSystemCancel
        AssignmentAction action,
        Long handymanId,
        @NullOrNotBlank
        String comment
) {
}