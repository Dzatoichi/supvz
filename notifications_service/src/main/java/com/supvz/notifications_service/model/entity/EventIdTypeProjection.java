package com.supvz.notifications_service.model.entity;

import java.util.UUID;

public interface EventIdTypeProjection {
    UUID getEventId();
    InboxEventType getEventType();
}
