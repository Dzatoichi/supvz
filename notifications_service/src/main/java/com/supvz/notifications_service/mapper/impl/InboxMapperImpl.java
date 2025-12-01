package com.supvz.notifications_service.mapper.impl;

import com.fasterxml.jackson.core.JsonProcessingException;
import com.fasterxml.jackson.databind.ObjectMapper;
import com.supvz.notifications_service.core.exception.InboxEventNotSerializedException;
import com.supvz.notifications_service.model.dto.InboxMessage;
import com.supvz.notifications_service.model.entity.InboxEvent;
import com.supvz.notifications_service.mapper.InboxMapper;
import lombok.RequiredArgsConstructor;
import lombok.extern.slf4j.Slf4j;
import org.springframework.stereotype.Component;

import java.time.LocalDateTime;

@Slf4j
@Component
@RequiredArgsConstructor
public class InboxMapperImpl implements InboxMapper {
    private final ObjectMapper objectMapper;

    @Override
    public InboxEvent create(InboxMessage event) {
        try {
            return InboxEvent.builder()
                    .eventId(event.eventId())
                    .eventType(event.eventType())
                    .payload(objectMapper.writeValueAsString(event.payload()))
                    .build();
        } catch (JsonProcessingException ex) {
            log.error("Couldn't serialize payload of event [{}].", event.eventId());
            throw new InboxEventNotSerializedException(ex.getMessage());
        }
    }

    @Override
    public void markAsProcessed(InboxEvent event) {
        event.setProcessedAt(LocalDateTime.now());
        event.setProcessed(true);
        event.setUpdatedAt(LocalDateTime.now());
        event.setReservedTo(null);
        event.setCleanAfter(null);
    }

    @Override
    public void setCleanAfter(InboxEvent event, LocalDateTime cleanAfter) {
        event.setCleanAfter(cleanAfter);
        event.setUpdatedAt(LocalDateTime.now());
        event.setReservedTo(null);
    }
}