package com.supvz.notifications_service.service;

import com.supvz.notifications_service.model.dto.InboxEventPayload;

import java.util.UUID;

public interface EventProcessingService {
    void initNotification(InboxEventPayload inboxEventPayload);

    void processNotification(UUID eventId);
}
