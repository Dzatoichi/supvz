package com.supvz.notifications_service.service;

import com.supvz.notifications_service.model.dto.InboxEventPayload;
import com.supvz.notifications_service.model.dto.NotificationPayload;

import java.util.UUID;

public interface EventProcessingService {
    void initNotification(InboxEventPayload inboxEventPayload, NotificationPayload notificationPayload);

    void processNotification(UUID eventId);

    void initOther(InboxEventPayload inboxEventPayload);
}
