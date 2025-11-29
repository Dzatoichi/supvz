package com.supvz.notifications_service.model.dto;


import com.supvz.notifications_service.model.entity.InboxEventType;
import jakarta.validation.Valid;
import jakarta.validation.constraints.NotNull;

import java.util.UUID;

public record InboxEventMessage(
        @NotNull
        UUID eventId,
        @NotNull
        InboxEventType eventType,
        @NotNull
        @Valid
        InboxEventPayload payload
) {
}