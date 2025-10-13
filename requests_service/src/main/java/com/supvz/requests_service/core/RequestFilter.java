package com.supvz.requests_service.core;

import lombok.Builder;

import java.util.UUID;

@Builder
/*
Схема (Payload) для фильтрации запросов.
 */
public record RequestFilter(
        Integer pvzId,
        UUID appellantId
) {
}
