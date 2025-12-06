package com.supvz.notifications_service.service.processor;

import com.supvz.notifications_service.model.entity.InboxEventType;

import java.util.UUID;

public interface InboxProcessor {
    void process(UUID eventId);
    InboxEventType getType();
}