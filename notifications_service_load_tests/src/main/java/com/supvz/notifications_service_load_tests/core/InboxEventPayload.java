package com.supvz.notifications_service_load_tests.core;


import java.util.UUID;

public record InboxEventPayload(
        UUID eventId,
        InboxEventType eventType,
        String payload
) {
}