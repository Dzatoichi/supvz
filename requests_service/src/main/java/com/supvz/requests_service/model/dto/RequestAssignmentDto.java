package com.supvz.requests_service.model.dto;

import io.swagger.v3.oas.annotations.media.Schema;
import com.supvz.requests_service.model.entity.enums.AssignmentAction;

import java.time.LocalDateTime;

@Schema(description = "Представление обращения на заявку (например, от исполнителя)")
public record RequestAssignmentDto(
        @Schema(description = "Уникальный идентификатор обращения", example = "123")
        long id,
        @Schema(description = "ID связанной заявки", example = "456")
        long requestId,
        @Schema(description = "ID исполнителя (мастера)", example = "789")
        long handymanId,
        @Schema(description = "Действие, выполненное по заявке")
        AssignmentAction action,
        @Schema(description = "Время обработки заявки")
        LocalDateTime processedAt,
        @Schema(description = "Время создания обращения")
        LocalDateTime createdAt,
        @Schema(description = "Время последнего обновления")
        LocalDateTime updatedAt,
        @Schema(description = "Комментарий к обращению", nullable = true)
        String comment
) {
}