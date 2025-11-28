package com.supvz.notifications_service.service;

import com.supvz.notifications_service.model.dto.NotificationDto;


public interface NotificationProcessingService {
    void send(NotificationDto notification);
}
