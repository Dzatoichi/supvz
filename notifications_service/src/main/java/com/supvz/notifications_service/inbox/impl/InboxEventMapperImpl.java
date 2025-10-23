package com.supvz.notifications_service.inbox.impl;

import com.supvz.notifications_service.core.dto.InboxEventDto;
import com.supvz.notifications_service.core.dto.MessageDto;
import com.supvz.notifications_service.entity.InboxEvent;
import com.supvz.notifications_service.inbox.InboxEventMapper;
import org.springframework.stereotype.Component;

@Component
public class InboxEventMapperImpl implements InboxEventMapper {
    @Override
    public InboxEvent create(MessageDto messageDto) {
        return InboxEvent.builder()
                .eventId(messageDto.eventId())
                .eventType(messageDto.eventType())
                .payload(messageDto.payload())
                .createdAt(messageDto.createdAt())
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