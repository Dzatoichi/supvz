package com.supvz.notifications_service.core.dto;

import lombok.Builder;

import java.time.LocalDateTime;

@Builder
public record NotificationDto(
        long id,
        String recipientId,
        String body,
        String subject,
        LocalDateTime sentAt,
        boolean viewed

) {
}
