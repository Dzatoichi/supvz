package com.supvz.notifications_service.service;

import com.supvz.notifications_service.core.dto.NotificationDto;
import com.supvz.notifications_service.core.dto.PageDto;
import com.supvz.notifications_service.core.filter.NotificationFilter;
import com.supvz.notifications_service.entity.InboxEvent;
import com.supvz.notifications_service.entity.Notification;

import java.time.LocalDateTime;
import java.util.UUID;

public interface NotificationService {
    void create(InboxEvent event);

    Notification getByEventId(UUID eventId);

    void markAsSent(Notification notification, LocalDateTime sentAndProcessedAt);

    PageDto<NotificationDto> findAll(int page, int size, NotificationFilter filter);
}
