package com.supvz.notifications_service.model.dto;

import com.supvz.notifications_service.model.entity.NotificationType;

public record NotificationPayload(
        NotificationType type,
        String recipientId,
        String body,
        String subject
) {
}