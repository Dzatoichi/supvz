package com.supvz.requests_service.model.dto;


import com.supvz.requests_service.core.enums.AssignmentAction;

import java.util.UUID;

/**
 * Схема (Payload) для обновления ответа на запрос.
 */
public record RequestAssignmentUpdatePayload(
        AssignmentAction action,
        Long handymanId,
        String comment
) {
}
// todo: хуета какая то схема