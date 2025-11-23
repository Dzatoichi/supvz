package com.supvz.notifications_service.inbox;

import com.supvz.notifications_service.model.dto.InboxEventDto;
import com.supvz.notifications_service.model.dto.InboxEventPayload;
import com.supvz.notifications_service.model.entity.InboxEvent;

public interface InboxEventMapper {
    InboxEvent create(InboxEventPayload inboxEventPayload);

    InboxEventDto read(InboxEvent inboxEvent);

    void markAsProcessed(InboxEvent event);

    void markAsFailed(InboxEvent event);
}
