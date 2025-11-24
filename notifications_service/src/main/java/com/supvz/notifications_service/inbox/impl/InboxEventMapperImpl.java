package com.supvz.notifications_service.inbox.impl;

import com.supvz.notifications_service.model.dto.InboxEventPayload;
import com.supvz.notifications_service.model.entity.InboxEvent;
import com.supvz.notifications_service.inbox.InboxEventMapper;
import org.springframework.stereotype.Component;

import java.time.LocalDateTime;

@Component
public class InboxEventMapperImpl implements InboxEventMapper {
    @Override
    public InboxEvent create(InboxEventPayload payload) {
        return InboxEvent.builder()
                .eventId(payload.eventId())
                .eventType(payload.eventType())
                .payload(payload.payload())
                .build();
    }

    @Override
    public void markAsProcessed(InboxEvent event) {
        event.setProcessedAt(LocalDateTime.now());
        event.setProcessed(true);
        event.setUpdatedAt(LocalDateTime.now());
        event.setReservedTo(null);
    }

    @Override
    public void setCleanAfter(InboxEvent event, LocalDateTime cleanAfter) {
        event.setCleanAfter(cleanAfter);
        event.setUpdatedAt(LocalDateTime.now());
        event.setReservedTo(null);
    }
}