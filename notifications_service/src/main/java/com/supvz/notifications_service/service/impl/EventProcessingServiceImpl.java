package com.supvz.notifications_service.service.impl;

import com.supvz.notifications_service.core.exception.NotificationConflictException;
import com.supvz.notifications_service.model.dto.InboxEventPayload;
import com.supvz.notifications_service.model.dto.NotificationPayload;
import com.supvz.notifications_service.model.entity.InboxEvent;
import com.supvz.notifications_service.inbox.InboxEventService;
import com.supvz.notifications_service.service.*;
import lombok.RequiredArgsConstructor;
import lombok.extern.slf4j.Slf4j;
import org.springframework.stereotype.Service;
import org.springframework.transaction.annotation.Transactional;

import java.util.UUID;

@Slf4j
@Service
@RequiredArgsConstructor
public class EventProcessingServiceImpl implements EventProcessingService {
    private final InboxEventService inboxEventService;
    private final NotificationService notificationService;

    @Override
    @Transactional
    public void initNotification(InboxEventPayload inboxEventPayload, NotificationPayload notificationPayload) {
        log.debug("Initialize notification message: [{}].", inboxEventPayload.eventId());
        InboxEvent inboxEvent = inboxEventService.create(inboxEventPayload);
        notificationService.create(inboxEvent, notificationPayload);
        log.info("Notification message [{}] is initialized.", inboxEventPayload.eventId());
    }

    @Override
    @Transactional
    public void processNotification(UUID eventId) {
        log.debug("Process notification by event [{}].", eventId);
        try {
            notificationService.processByEventId(eventId);
            inboxEventService.setProcessed(eventId);
            log.info("Notification event [{}] is processed.", eventId);
        } catch (NotificationConflictException ex) {
            log.warn("Conflict: {}", ex.getMessage());
            inboxEventService.setProcessed(eventId);
        }
        catch (RuntimeException e) {
            log.error("Couldn't successfully process notification by event [{}]", eventId, e);
            inboxEventService.setCleanAfter(eventId);
        }
    }
//    todo: жестко подумать про вложенные транзакции

    @Override
    public void initOther(InboxEventPayload inboxEventPayload) {
        log.debug("Listening other event type. Event [{}].", inboxEventPayload.eventId());
    }
}
