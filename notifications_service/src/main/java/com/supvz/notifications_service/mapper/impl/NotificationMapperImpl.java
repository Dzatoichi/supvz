package com.supvz.notifications_service.mapper.impl;

import com.fasterxml.jackson.databind.ObjectMapper;
import com.supvz.notifications_service.core.dto.NotificationDto;
import com.supvz.notifications_service.core.dto.PageDto;
import com.supvz.notifications_service.core.exception.InvalidMessagePatternException;
import com.supvz.notifications_service.core.dto.MessagePayloadDto;
import com.supvz.notifications_service.entity.InboxEvent;
import com.supvz.notifications_service.entity.Notification;
import com.supvz.notifications_service.entity.NotificationType;
import com.supvz.notifications_service.mapper.NotificationMapper;
import lombok.RequiredArgsConstructor;
import lombok.extern.slf4j.Slf4j;
import org.springframework.data.domain.Page;
import org.springframework.stereotype.Component;

import java.io.IOException;
import java.util.List;

@Slf4j
@Component
@RequiredArgsConstructor
public class NotificationMapperImpl implements NotificationMapper {
    private final ObjectMapper objectMapper;

    @Override
    public Notification create(InboxEvent event) {
        try {
            MessagePayloadDto payload = objectMapper.readValue(event.getPayload(), MessagePayloadDto.class);

            Notification build = Notification.builder()
                    .event(event)
                    .notificationType(event.getEventType())
                    .body(payload.body())
                    .subject(payload.subject())
                    .recipientId(payload.recipientId())
                    .build();
            if (event.getEventType() == NotificationType.push || event.getEventType() == NotificationType.web) {
                build.setViewed(false);
            }
            return build;
        } catch (IOException e) {
            throw new InvalidMessagePatternException("Failed to deserialize" +
                    " payload [%s] of event [%s].".formatted(event.getPayload(), event.getEventId()));
        }
    }

    @Override
    public NotificationDto read(Notification notification) {
        return NotificationDto.builder()
                .id(notification.getId())
                .body(notification.getBody())
                .subject(notification.getSubject())
                .viewed(notification.getViewed())
                .sentAt(notification.getSentAt())
                .recipientId(notification.getRecipientId())
                .build();
    }

    @Override
    public PageDto<NotificationDto> readPage(Page<Notification> page) {
        List<NotificationDto> content = page.getContent().stream().map(this::read).toList();
        return PageDto.<NotificationDto>builder()
                .content(content)
                .page(page.getNumber())
                .size(page.getSize())
                .total(page.getTotalPages())
                .hasNext(page.hasNext())
                .hasPrev(page.hasPrevious())
                .build();
    }
}
