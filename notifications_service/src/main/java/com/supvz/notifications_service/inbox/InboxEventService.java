package com.supvz.notifications_service.inbox;

import com.supvz.notifications_service.model.dto.InboxEventPayload;
import com.supvz.notifications_service.model.entity.InboxEvent;

import java.util.List;
import java.util.UUID;

public interface InboxEventService {
    InboxEvent create(InboxEventPayload inboxEventPayload);

    List<UUID> readAndReserveUnprocessedBatch(int batchSize);

    void setProcessed(UUID eventId);

    void setCleanAfter(UUID eventId);

    List<UUID> deleteFailedBatch(Integer batchSize);
}
