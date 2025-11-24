package com.supvz.notifications_service.inbox;

import com.supvz.notifications_service.model.dto.InboxEventPayload;
import com.supvz.notifications_service.model.entity.InboxEvent;

import java.time.LocalDateTime;

public interface InboxEventMapper {
    InboxEvent create(InboxEventPayload inboxEventPayload);

    void markAsProcessed(InboxEvent event);

    void setCleanAfter(InboxEvent event, LocalDateTime cleanAfter);
}
