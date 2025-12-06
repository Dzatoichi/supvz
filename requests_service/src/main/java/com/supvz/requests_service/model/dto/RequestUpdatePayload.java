package com.supvz.requests_service.model.dto;


/*
Схема (Payload) для обновления запроса мастеру.
 */
public record RequestUpdatePayload(
        Integer pvzId,
        String description
) {
}
