package com.supvz.notifications_service.mapper.impl;

import com.fasterxml.jackson.databind.ObjectMapper;
import com.supvz.notifications_service.core.exception.InvalidMessagePatternException;
import com.supvz.notifications_service.core.dto.MessagePayloadDto;
import com.supvz.notifications_service.entity.InboxEvent;
import com.supvz.notifications_service.entity.Notification;
import com.supvz.notifications_service.mapper.NotificationMapper;
import lombok.RequiredArgsConstructor;
import lombok.extern.slf4j.Slf4j;
import org.springframework.stereotype.Component;

import java.io.IOException;

@Slf4j
@Component
@RequiredArgsConstructor
public class NotificationMapperImpl implements NotificationMapper {
    private final ObjectMapper objectMapper;

    @Override
    public Notification create(InboxEvent event) {
        try {
            MessagePayloadDto payload = objectMapper.readValue(event.getPayload(), MessagePayloadDto.class);

            return Notification.builder()
                    .event(event)
                    .notificationType(event.getEventType())
                    .body(payload.body())
                    .subject(payload.subject())
                    .recipientId(payload.recipientId())
                    .build();

        } catch (IOException e) {
            throw new InvalidMessagePatternException("Failed to deserialize" +
                    " payload [%s] of event [%s].".formatted(event.getPayload(), event.getEventId()));
        }
    }
}
