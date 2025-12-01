package com.supvz.notifications_service.service;

import com.supvz.notifications_service.model.dto.InboxMessage;
import com.supvz.notifications_service.model.entity.EventIdTypeProjection;
import com.supvz.notifications_service.model.entity.InboxEvent;

import java.util.List;
import java.util.UUID;

public interface InboxService {
    InboxEvent create(InboxMessage inboxMessage);

    List<EventIdTypeProjection> readAndReserveUnprocessedBatch(int batchSize);

    void setProcessed(UUID eventId);

    void setCleanAfter(UUID eventId);

    List<UUID> deleteFailedBatch(Integer batchSize);
}
