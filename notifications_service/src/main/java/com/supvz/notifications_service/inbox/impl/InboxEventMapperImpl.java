package com.supvz.notifications_service.inbox.impl;

import com.supvz.notifications_service.model.dto.InboxEventDto;
import com.supvz.notifications_service.model.dto.InboxEventPayload;
import com.supvz.notifications_service.model.entity.InboxEvent;
import com.supvz.notifications_service.inbox.InboxEventMapper;
import org.springframework.stereotype.Component;

@Component
public class InboxEventMapperImpl implements InboxEventMapper {
    @Override
    public InboxEvent create(InboxEventPayload inboxEventPayload) {
        return InboxEvent.builder()
                .eventId(inboxEventPayload.eventId())
                .eventType(inboxEventPayload.eventType())
                .payload(inboxEventPayload.payload())
                .createdAt(inboxEventPayload.createdAt())
                .build();
    }

    @Override
    public InboxEventDto read(InboxEvent inboxEvent) {
        return InboxEventDto.builder()
                .eventId(inboxEvent.getEventId())
                .eventType(inboxEvent.getEventType())
                .build();
    }
}