package com.supvz.notifications_service_load_tests.core;

public record NotificationPayload(
        NotificationType type,
        String recipientId,
        String body,
        String subject
) {
}
