package com.supvz.requests_service.model.dto;

import io.swagger.v3.oas.annotations.media.Schema;
import com.supvz.requests_service.core.annotation.NullOrNotBlank;
import jakarta.validation.constraints.NotNull;

@Schema(description = "Данные для создания нового обращения на заявку")
public record RequestAssignmentPayload(
        @Schema(description = "ID заявки, к которой привязывается обращение", example = "456")
        @NotNull
        long requestId,
        @Schema(description = "ID исполнителя (мастера)", example = "789")
        @NotNull
        long handymanId,
        @Schema(description = "Комментарий (может быть null или пустым)", nullable = true)
        @NullOrNotBlank
        String comment
) {
}