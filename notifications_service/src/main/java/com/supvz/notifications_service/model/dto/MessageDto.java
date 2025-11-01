package com.supvz.notifications_service.model.dto;


import com.supvz.notifications_service.model.entity.NotificationType;

import java.time.LocalDateTime;
import java.util.UUID;

public record MessageDto (
        UUID eventId,
        NotificationType eventType,
        String payload,
        LocalDateTime createdAt
) {
}
