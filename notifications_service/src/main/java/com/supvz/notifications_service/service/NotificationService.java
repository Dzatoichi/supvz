package com.supvz.notifications_service.service;

import com.supvz.notifications_service.entity.InboxEvent;
import com.supvz.notifications_service.entity.Notification;

public interface NotificationService {
    Notification create(InboxEvent event);
}
