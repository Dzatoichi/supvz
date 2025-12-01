package com.supvz.notifications_service.service.impl;

import com.supvz.notifications_service.model.dto.NotificationDto;
import com.supvz.notifications_service.model.entity.NotificationType;
import com.supvz.notifications_service.service.NotificationProcessor;
import lombok.extern.slf4j.Slf4j;
import org.springframework.retry.annotation.Retryable;
import org.springframework.stereotype.Service;
import org.springframework.transaction.annotation.Propagation;
import org.springframework.transaction.annotation.Transactional;

@Slf4j
@Service
public class PushNotificationProcessor implements NotificationProcessor {
    @Override
//    @Retryable(retryFor = RuntimeException.class, maxAttemptsExpression = "${app.notification.number-retry-attempts}")
    @Transactional(propagation = Propagation.NOT_SUPPORTED)
    public void send(NotificationDto notification) {
        log.debug("Sending push notification [{}].", notification.id());
    }

    @Override
    public NotificationType getType() {
        return NotificationType.push;
    }
}
