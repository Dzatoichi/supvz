package com.supvz.notifications_service.service;

import com.supvz.notifications_service.entity.InboxEvent;

import java.util.UUID;

public interface NotificationService {
    void create(InboxEvent event);

    void process(UUID eventId);
}
