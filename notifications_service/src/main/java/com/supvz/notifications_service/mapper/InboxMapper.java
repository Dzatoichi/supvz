package com.supvz.notifications_service.mapper;

import com.supvz.notifications_service.model.dto.InboxMessage;
import com.supvz.notifications_service.model.entity.InboxEvent;

import java.time.LocalDateTime;

public interface InboxMapper {
    InboxEvent create(InboxMessage inboxMessage);

    void markAsProcessed(InboxEvent event);

    void setCleanAfter(InboxEvent event, LocalDateTime cleanAfter);
}
