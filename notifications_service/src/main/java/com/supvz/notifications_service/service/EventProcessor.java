package com.supvz.notifications_service.service;

import com.supvz.notifications_service.model.dto.InboxEventMessage;
import com.supvz.notifications_service.model.dto.NotificationPayload;

import java.util.UUID;

public interface EventProcessor {
    void initNotification(InboxEventMessage inboxEventMessage, NotificationPayload notificationPayload);

    void processNotification(UUID eventId);

    void initOther(InboxEventMessage inboxEventMessage);
}
