package com.supvz.requests_service.model.dto;

import io.swagger.v3.oas.annotations.media.Schema;
import com.supvz.requests_service.model.entity.enums.RequestStatus;

@Schema(description = "Упрощённое представление заявки (без вложенных обращений)")
public record RequestPlainDto(
        @Schema(description = "Уникальный идентификатор заявки", example = "101")
        long id,
        @Schema(description = "ID ПВЗ", example = "202")
        int pvzId,
        @Schema(description = "ID заявителя", example = "303")
        long appellantId,
        @Schema(description = "Текущий статус заявки")
        RequestStatus status,
        @Schema(description = "Краткое название проблемы", example = "Не работает терминал")
        String subject,
        @Schema(description = "Подробное описание проблемы", nullable = true)
        String description
) {
}