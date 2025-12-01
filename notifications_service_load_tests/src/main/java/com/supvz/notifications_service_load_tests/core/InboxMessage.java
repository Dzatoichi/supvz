package com.supvz.notifications_service_load_tests.core;


import java.util.UUID;

public record InboxMessage(
        UUID eventId,
        InboxEventType eventType,
        NotificationPayload payload
) {
}