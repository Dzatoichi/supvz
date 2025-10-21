package com.supvz.notifications_service.service.impl;

import com.supvz.notifications_service.entity.InboxEvent;
import com.supvz.notifications_service.entity.Notification;
import com.supvz.notifications_service.service.NotificationService;
import lombok.extern.slf4j.Slf4j;
import org.springframework.stereotype.Service;

import java.util.UUID;

@Slf4j
@Service
public class NotificationServiceImpl implements NotificationService {
    @Override
    public Notification create(InboxEvent event) {
        log.info("CREATE NOTIFICATION BY TYPE [{}], BY EVENT [{}].", event.getEventType(), event.getEventId());
        log.info("NOTIFICATION [{}] BY EVENT [{}] IS CREATED.", UUID.randomUUID(), event.getEventId());
        return null;
    }
}
