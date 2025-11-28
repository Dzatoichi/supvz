package com.supvz.notifications_service.service;

import com.supvz.notifications_service.core.exception.NotificationIsNotSentException;
import com.supvz.notifications_service.core.exception.UnexpectedExceptionSendingNotification;
import com.supvz.notifications_service.model.dto.NotificationDto;
import com.supvz.notifications_service.model.dto.NotificationPayload;
import com.supvz.notifications_service.model.dto.PageDto;
import com.supvz.notifications_service.core.filter.NotificationFilter;
import com.supvz.notifications_service.model.entity.InboxEvent;

import java.util.UUID;

public interface NotificationService {
    void create(InboxEvent event, NotificationPayload notificationPayload);

    PageDto<NotificationDto> findAll(int page, int size, NotificationFilter filter);

    void processByEventId(UUID eventId) throws NotificationIsNotSentException, UnexpectedExceptionSendingNotification;
}
