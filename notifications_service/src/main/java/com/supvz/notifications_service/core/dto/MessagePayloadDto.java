package com.supvz.notifications_service.core.dto;

public record MessagePayloadDto(
        String recipientId,
        String body,
        String subject
) {
}
