package com.supvz.notifications_service.service;

import com.supvz.notifications_service.entity.InboxEvent;
import com.supvz.notifications_service.entity.Notification;

import java.time.LocalDateTime;
import java.util.UUID;

public interface NotificationService {
    void create(InboxEvent event);

    Notification findByEventId(UUID eventId);

    void markSent(Notification notification, LocalDateTime sentAndProcessedAt);
}
