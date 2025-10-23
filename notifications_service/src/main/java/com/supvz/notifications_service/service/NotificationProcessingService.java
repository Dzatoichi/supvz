package com.supvz.notifications_service.service;

import com.supvz.notifications_service.core.dto.MessageDto;
import com.supvz.notifications_service.entity.Notification;

public interface NotificationProcessingService {
    void init(MessageDto messageDto);

    void process(Notification notification);
}
