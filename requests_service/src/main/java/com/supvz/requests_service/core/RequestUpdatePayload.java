package com.supvz.requests_service.core;


/*
Схема (Payload) для обновления запроса мастеру.
 */
public record RequestUpdatePayload(
        Integer pvzId,
        String description
) {
}
