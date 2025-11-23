package com.supvz.notifications_service.model.dto;

import com.supvz.notifications_service.model.entity.InboxEventType;
import lombok.Builder;

import java.util.UUID;

@Builder
public record InboxEventDto(
        UUID eventId,
        InboxEventType eventType
) {
}
