package com.supvz.notifications_service.core.filter;

import com.supvz.notifications_service.entity.NotificationType;

import java.time.LocalDateTime;
import java.util.UUID;

public record NotificationFilter(
        UUID eventId,
        NotificationType type,
        String recipientId,
        LocalDateTime sentAt,
        DateNotificationFilter dateFilter,
        Boolean viewed
) {
}
