package com.supvz.notifications_service.model.dto;


import com.supvz.notifications_service.model.entity.InboxEventType;

import java.util.UUID;

public record InboxEventPayload(
        UUID eventId,
        InboxEventType eventType,
        String payload
) {
}