package com.supvz.notifications_service.model.dto;


import com.supvz.notifications_service.model.entity.InboxEventType;

import java.util.UUID;

public record InboxMessage(
        UUID eventId,
        InboxEventType eventType,
        String payload
) {
}