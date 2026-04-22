package com.supvz.requests_service.model.dto;

import io.swagger.v3.oas.annotations.media.Schema;
import com.supvz.requests_service.core.annotation.EmptyOrSize;
import com.supvz.requests_service.core.annotation.NullOrNotBlank;

@Schema(description = "Частичное обновление заявки")
public record RequestUpdatePayload(
        @Schema(description = "Новый ID ПВЗ (если меняется)", nullable = true, example = "999")
        Integer pvzId,
        @Schema(description = "Обновлённое краткое название (5–64 символа)", nullable = true, example = "Wi-Fi не ловит")
        @EmptyOrSize(min = 5, max = 64)
        @NullOrNotBlank
        String subject,
        @Schema(description = "Обновлённое описание", nullable = true)
        @NullOrNotBlank
        String description
) {}