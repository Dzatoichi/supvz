package com.supvz.notifications_service.mapper.impl;

import com.fasterxml.jackson.databind.ObjectMapper;
import com.supvz.notifications_service.model.dto.NotificationDto;
import com.supvz.notifications_service.model.dto.PageDto;
import com.supvz.notifications_service.model.dto.NotificationPayload;
import com.supvz.notifications_service.model.entity.InboxEvent;
import com.supvz.notifications_service.model.entity.Notification;
import com.supvz.notifications_service.model.entity.NotificationType;
import com.supvz.notifications_service.mapper.NotificationMapper;
import lombok.RequiredArgsConstructor;
import lombok.extern.slf4j.Slf4j;
import org.springframework.data.domain.Page;
import org.springframework.stereotype.Component;

import java.time.LocalDateTime;
import java.util.List;

@Slf4j
@Component
@RequiredArgsConstructor
public class NotificationMapperImpl implements NotificationMapper {
    private final ObjectMapper objectMapper;

    @Override
    public Notification create(InboxEvent event, NotificationPayload payload) {
        NotificationType type = payload.type();
        Notification build = Notification.builder()
                .event(event)
                .notificationType(type)
                .body(payload.body())
                .subject(payload.subject())
                .recipientId(payload.recipientId())
                .build();
        if (type == NotificationType.push || type == NotificationType.web) {
            build.setViewed(false);
        }
        return build;
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
    public void markAsSent(Notification notification) {
        if (notification.getSent())
            return;
        notification.setSentAt(LocalDateTime.now());
        notification.setSent(true);
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
