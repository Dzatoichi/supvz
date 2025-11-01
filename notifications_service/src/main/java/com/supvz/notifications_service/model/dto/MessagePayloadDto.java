package com.supvz.notifications_service.model.dto;

public record MessagePayloadDto(
        String recipientId,
        String body,
        String subject
) {
}
