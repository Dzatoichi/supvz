package com.supvz.notifications_service.service;

import com.supvz.notifications_service.model.dto.NotificationDto;
import com.supvz.notifications_service.model.entity.NotificationType;


public interface NotificationProcessor {
    void send(NotificationDto notification);

    NotificationType getType();
}
