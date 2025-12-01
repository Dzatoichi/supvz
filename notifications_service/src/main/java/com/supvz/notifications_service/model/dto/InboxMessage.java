package com.supvz.notifications_service.model.dto;


import com.fasterxml.jackson.databind.annotation.JsonDeserialize;
import com.supvz.notifications_service.model.entity.InboxEventType;
import com.supvz.notifications_service.util.KeepAsJsonStringDeserializer;

import java.util.UUID;

public record InboxMessage(
        UUID eventId,
        InboxEventType eventType,
        @JsonDeserialize(using = KeepAsJsonStringDeserializer.class)
        String payload
) {
}