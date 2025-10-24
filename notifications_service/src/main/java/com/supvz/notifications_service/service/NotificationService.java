package com.supvz.notifications_service.service;

import com.supvz.notifications_service.entity.InboxEvent;
import com.supvz.notifications_service.entity.Notification;

import java.util.UUID;

public interface NotificationService {
    void create(InboxEvent event);

    Notification findByEventId(UUID eventId);
}
