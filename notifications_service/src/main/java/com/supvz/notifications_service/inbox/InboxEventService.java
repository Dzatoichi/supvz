package com.supvz.notifications_service.inbox;

import com.supvz.notifications_service.model.dto.InboxEventPayload;
import com.supvz.notifications_service.model.entity.InboxEvent;

import java.time.LocalDateTime;
import java.util.List;
import java.util.UUID;

public interface InboxEventService {
    InboxEvent create(InboxEventPayload inboxEventPayload);

    List<UUID> readAndReserveUnprocessedBatch(int batchSize);

    void reserveEvent(InboxEvent event);

    void markProcessed(InboxEvent event, LocalDateTime sentAndProcessedAt);

    InboxEvent getById(UUID eventId);
}
