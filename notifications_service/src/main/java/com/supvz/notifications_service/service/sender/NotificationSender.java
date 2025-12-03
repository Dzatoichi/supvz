package com.supvz.notifications_service.service.sender;

import com.supvz.notifications_service.model.dto.NotificationDto;
import com.supvz.notifications_service.model.entity.NotificationType;


public interface NotificationSender {
    void send(NotificationDto notification);

    NotificationType getType();
}
