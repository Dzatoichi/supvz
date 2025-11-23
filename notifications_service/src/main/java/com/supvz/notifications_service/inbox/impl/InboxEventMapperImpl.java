package com.supvz.notifications_service.inbox.impl;

import com.supvz.notifications_service.model.dto.InboxEventDto;
import com.supvz.notifications_service.model.dto.InboxEventPayload;
import com.supvz.notifications_service.model.entity.InboxEventStatus;
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
    public InboxEventDto read(InboxEvent event) {
        return InboxEventDto.builder()
                .eventId(event.getEventId())
                .eventType(event.getEventType())
                .build();
    }

    @Override
    public void markAsProcessed(InboxEvent event) {
        event.setProcessedAt(LocalDateTime.now());
        event.setProcessed(true);
        event.setStatus(InboxEventStatus.success);
    }

    @Override
    public void markAsFailed(InboxEvent event) {
        event.setProcessedAt(LocalDateTime.now());
        event.setProcessed(true);
        event.setStatus(InboxEventStatus.failed);
    }
}