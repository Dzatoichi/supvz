package com.supvz.notifications_service.service;

import com.supvz.notifications_service.model.entity.InboxEventType;

import java.util.UUID;

public interface InboxProcessor {
    void process(UUID eventId);
    InboxEventType getType();
}
