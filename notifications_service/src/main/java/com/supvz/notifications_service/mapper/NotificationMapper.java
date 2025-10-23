package com.supvz.notifications_service.mapper;

import com.supvz.notifications_service.entity.InboxEvent;
import com.supvz.notifications_service.entity.Notification;

public interface NotificationMapper {
    Notification create(InboxEvent event);
}
