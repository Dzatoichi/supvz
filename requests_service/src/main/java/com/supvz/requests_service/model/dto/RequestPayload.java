package com.supvz.requests_service.model.dto;

import io.swagger.v3.oas.annotations.media.Schema;
import com.supvz.requests_service.core.annotation.NullOrNotBlank;
import com.supvz.requests_service.core.annotation.EmptyOrSize;
import jakarta.validation.constraints.NotNull;

@Schema(description = "Данные для создания новой заявки")
public record RequestPayload(
        @Schema(description = "ID ПВЗ", example = "123")
        @NotNull
        int pvzId,
        @Schema(description = "ID заявителя", example = "456")
        @NotNull
        long appellantId,
        @Schema(description = "Краткое название (5–64 символа)", example = "Проблема с Wi-Fi")
        @EmptyOrSize(min = 5, max = 64)
        @NullOrNotBlank
        String subject,
        @Schema(description = "Подробное описание (может быть пустым)", nullable = true)
        @NullOrNotBlank
        String description
) {
}