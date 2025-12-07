package com.supvz.requests_service.model.dto;

import java.util.List;


/**
 * ДТО-представление заявки для перемещения между слоями, приложениями.
 */
public record RequestDto(
        long id,
        int pvzId,
        long appellantId,
        String subject,
        String description,
        List<RequestAssignmentDto> assignments
//        todo: ошибка передавать просто молча все ответы на эту заявку
) {
}
