package com.supvz.notifications_service.mapper;

import com.supvz.notifications_service.core.dto.NotificationDto;
import com.supvz.notifications_service.core.dto.PageDto;
import com.supvz.notifications_service.entity.InboxEvent;
import com.supvz.notifications_service.entity.Notification;
import org.springframework.data.domain.Page;

public interface NotificationMapper {
    Notification create(InboxEvent event);

    PageDto<NotificationDto> readPage(Page<Notification> notificationPage);

    NotificationDto read(Notification notification);
}
