package com.supvz.notifications_service.mapper;

import com.supvz.notifications_service.model.dto.NotificationDto;
import com.supvz.notifications_service.model.dto.NotificationPayload;
import com.supvz.notifications_service.model.dto.PageDto;
import com.supvz.notifications_service.model.entity.InboxEvent;
import com.supvz.notifications_service.model.entity.Notification;
import org.springframework.data.domain.Page;

public interface NotificationMapper {
    Notification create(InboxEvent event, NotificationPayload notificationPayload);

    PageDto<NotificationDto> readPage(Page<Notification> notificationPage);

    NotificationDto read(Notification notification);

    void markAsSent(Notification notification);
}
