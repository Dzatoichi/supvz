package com.supvz.requests_service.model.dto;


import com.supvz.requests_service.core.annotation.EmptyOrSize;
import com.supvz.requests_service.core.annotation.NullOrNotBlank;

/**
 * Схема обновления запроса.
 */
public record RequestUpdatePayload(
        Integer pvzId,
        @EmptyOrSize(min = 5, max = 64)
        @NullOrNotBlank
        String subject,
        @NullOrNotBlank
        String description
) {
}