package com.supvz.notifications_service.model.dto;

import com.supvz.notifications_service.model.entity.NotificationType;
import lombok.Builder;

import java.time.LocalDateTime;

@Builder
public record NotificationDto(
        long id,
        String recipientId,
        String body,
        String subject,
        LocalDateTime sentAt,
        Boolean viewed,
        NotificationType notificationType
) {
}
