package com.supvz.notifications_service.core.dto;

import com.supvz.notifications_service.entity.NotificationType;
import lombok.Builder;

import java.util.UUID;

@Builder
public record InboxEventDto(
        UUID eventId,
        NotificationType eventType
) {
}
