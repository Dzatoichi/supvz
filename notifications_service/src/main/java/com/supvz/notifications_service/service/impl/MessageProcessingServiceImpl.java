package com.supvz.notifications_service.service.impl;

import com.supvz.notifications_service.core.dto.MessageDto;
import com.supvz.notifications_service.entity.InboxEvent;
import com.supvz.notifications_service.entity.Notification;
import com.supvz.notifications_service.inbox.InboxEventService;
import com.supvz.notifications_service.service.*;
import lombok.RequiredArgsConstructor;
import lombok.extern.slf4j.Slf4j;
import org.springframework.stereotype.Service;
import org.springframework.transaction.annotation.Transactional;

import java.time.LocalDateTime;
import java.util.UUID;

@Slf4j
@Service
@RequiredArgsConstructor
public class MessageProcessingServiceImpl implements MessageProcessingService {
    private final InboxEventService inboxEventService;
    private final NotificationService notificationService;
    private final EmailNotificationProcessingService emailNotificationService;
    private final WebNotificationProcessingService webNotificationService;
    private final PushNotificationProcessingService pushNotificationService;

    @Override
    @Transactional
    public void initNotification(MessageDto messageDto) {
        log.debug("Initialize notification message: [{}].", messageDto.eventId());

        InboxEvent inboxEvent = inboxEventService.create(messageDto);
        notificationService.create(inboxEvent);

        log.info("Notification message [{}] is initialized.", messageDto.eventId());
    }

    @Override
    @Transactional
    public void processNotification(UUID eventId) {
        log.debug("Process notification by event [{}].", eventId);

        Notification notification = notificationService.getByEventId(eventId);
        switch (notification.getNotificationType()) {
            case email -> emailNotificationService.send(notification);
            case web -> webNotificationService.send(notification);
            case push -> pushNotificationService.send(notification);
        }
        LocalDateTime sentAndProcessedAt = LocalDateTime.now();
        notificationService.markAsSent(notification, sentAndProcessedAt);
        inboxEventService.markProcessed(notification.getEvent(), sentAndProcessedAt);

        log.info("Notification [{}] by event [{}] is processed.", notification.getId(), eventId);
    }
}
