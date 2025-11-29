package com.supvz.notifications_service.service.impl;

import com.supvz.notifications_service.core.exception.NotificationConflictException;
import com.supvz.notifications_service.core.exception.NotificationIsNotSentException;
import com.supvz.notifications_service.model.dto.InboxEventMessage;
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
public class InboxEventProcessor implements EventProcessor {
    private final InboxEventService inboxEventService;
    private final NotificationService notificationService;

    @Override
    @Transactional
    public void initNotification(InboxEventMessage inboxEventMessage, NotificationPayload notificationPayload) {
        log.debug("Initialize notification message: [{}].", inboxEventMessage.eventId());
        InboxEvent inboxEvent = inboxEventService.create(inboxEventMessage);
        notificationService.create(inboxEvent, notificationPayload);
        log.info("Notification message [{}] is initialized.", inboxEventMessage.eventId());
    }

    @Override
    public void processNotification(UUID eventId) {
        log.debug("Process notification by event [{}].", eventId);
        try {
            notificationService.processByEventId(eventId);
            inboxEventService.setProcessed(eventId);
            log.info("Notification event [{}] is processed.", eventId);
        } catch (NotificationConflictException ex) {
            log.warn("Conflict: {}", ex.getMessage());
            inboxEventService.setProcessed(eventId);
        } catch (NotificationIsNotSentException ex) {
            log.warn("Couldn't successfully process notification by event [{}]", eventId, ex);
            inboxEventService.setCleanAfter(eventId);
        } catch (RuntimeException ex) {
            log.error("Unexpected runtime exception while processing notification by event [{}]", eventId, ex);
            inboxEventService.setCleanAfter(eventId);
        }
    }

    @Override
    public void initOther(InboxEventMessage inboxEventMessage) {
        log.debug("Listening other event type. Event [{}].", inboxEventMessage.eventId());
    }
}