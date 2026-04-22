package com.supvz.notifications_service.core.filter;

import com.supvz.notifications_service.model.entity.NotificationType;

import java.time.LocalDateTime;
import java.util.UUID;

public record NotificationFilter(
        UUID eventId,
        NotificationType type,
        String recipientId,
        String subject,
        String body,
        Boolean viewed,
        Boolean sent,
        LocalDateTime startDate,
        LocalDateTime endDate
) {
}