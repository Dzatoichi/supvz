package com.supvz.notifications_service.service.impl;

import com.supvz.notifications_service.model.dto.NotificationDto;
import com.supvz.notifications_service.service.PushNotificationProcessingService;
import lombok.extern.slf4j.Slf4j;
import org.springframework.stereotype.Service;

@Slf4j
@Service
public class PushNotificationProcessingServiceImpl implements PushNotificationProcessingService {
    @Override
    public void send(NotificationDto notification) {
        log.debug("Sending push notification [{}].", notification.id());
    }
}
