package com.supvz.notifications_service.inbox;

import com.supvz.notifications_service.model.dto.InboxEventMessage;
import com.supvz.notifications_service.model.entity.InboxEvent;

import java.time.LocalDateTime;

public interface InboxEventMapper {
    InboxEvent create(InboxEventMessage inboxEventMessage);

    void markAsProcessed(InboxEvent event);

    void setCleanAfter(InboxEvent event, LocalDateTime cleanAfter);
}
