package com.supvz.requests_service.model.dto;

import com.supvz.requests_service.model.entity.enums.RequestStatus;

import java.util.List;


/**
 * ДТО-представление заявки для перемещения между слоями, приложениями.
 */
public record RequestDto(
        long id,
        int pvzId,
        long appellantId,
        RequestStatus status,
        String subject,
        String description,
        List<RequestAssignmentDto> assignments
) {
}