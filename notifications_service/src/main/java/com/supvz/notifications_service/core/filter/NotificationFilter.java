package com.supvz.notifications_service.core.filter;

import com.supvz.notifications_service.model.entity.NotificationType;

import java.util.UUID;

public record NotificationFilter(
        UUID eventId,
        NotificationType type,
        String recipientId,
        DateNotificationFilter dateFilter,
        Boolean viewed
) {
}
