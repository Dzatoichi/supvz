package com.supvz.notifications_service.service;

import com.supvz.notifications_service.model.entity.Notification;


public interface NotificationProcessingService {
    void send(Notification notification);
}
