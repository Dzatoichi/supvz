package com.supvz.notifications_service.service.impl;

import com.supvz.notifications_service.core.dto.MessageDto;
import com.supvz.notifications_service.entity.InboxEvent;
import com.supvz.notifications_service.entity.Notification;
import com.supvz.notifications_service.inbox.InboxEventService;
import com.supvz.notifications_service.service.NotificationProcessingService;
import com.supvz.notifications_service.service.NotificationService;
import lombok.RequiredArgsConstructor;
import lombok.extern.slf4j.Slf4j;
import org.springframework.stereotype.Service;
import org.springframework.transaction.annotation.Transactional;

@Slf4j
@Service
@RequiredArgsConstructor
public class NotificationProcessingServiceImpl implements NotificationProcessingService {
    private final InboxEventService inboxEventService;
    private final NotificationService notificationService;

    @Override
    @Transactional
    public void init(MessageDto messageDto) {
        log.info("Initialize notification message: [{}].", messageDto.eventId());

        InboxEvent inboxEvent = inboxEventService.create(messageDto);
        notificationService.create(inboxEvent);

        log.info("Notification message [{}] is initialized.", messageDto.eventId());
    }

    @Override
    public void process(Notification notification) {

    }
}
