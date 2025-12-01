package com.supvz.notifications_service.service;

import com.supvz.notifications_service.model.dto.NotificationDto;
import com.supvz.notifications_service.model.dto.NotificationPayload;
import com.supvz.notifications_service.model.dto.PageDto;
import com.supvz.notifications_service.core.filter.NotificationFilter;
import com.supvz.notifications_service.model.entity.InboxEvent;

import java.util.List;
import java.util.UUID;

public interface NotificationService {
    void create(InboxEvent event, NotificationPayload notificationPayload);

    PageDto<NotificationDto> findAll(int page, int size, NotificationFilter filter);

    void processByEventId(UUID eventId);

    List<Integer> deleteOldNotifications();
}
