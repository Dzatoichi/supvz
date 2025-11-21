package com.supvz.notifications_service.service.impl;

import com.supvz.notifications_service.model.dto.MessageDto;
import com.supvz.notifications_service.model.entity.InboxEvent;
import com.supvz.notifications_service.model.entity.Notification;
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
public class EventProcessingServiceImpl implements EventProcessingService {
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
//        todo: а что если дубль прошел и уже такой существует?

        log.info("Notification message [{}] is initialized.", messageDto.eventId());
    }

    @Override
    @Transactional
    public void processNotification(UUID eventId) {
        log.debug("Process notification by event [{}].", eventId);

        Notification notification = notificationService.getByEventId(eventId);
//        todo: ну а если нотификация не найдена? тоже надо учесть. исключение перехватить и че то сделать
        switch (notification.getNotificationType()) {
            case email -> emailNotificationService.send(notification);
            case web -> webNotificationService.send(notification);
            case push -> pushNotificationService.send(notification);
        }

//        todo: рассмотреть сценарий, если уведомление не обработалось, перехват исключения в send. придумать компенсирующие события. обработчики ошибок

        LocalDateTime sentAndProcessedAt = LocalDateTime.now();
        notificationService.markAsSent(notification, sentAndProcessedAt);
        inboxEventService.markProcessed(notification.getEvent(), sentAndProcessedAt);
//        todo: обработка и отметка нотификации должна выполняться атомарно.

        log.info("Notification [{}] by event [{}] is processed.", notification.getId(), eventId);
    }
}
