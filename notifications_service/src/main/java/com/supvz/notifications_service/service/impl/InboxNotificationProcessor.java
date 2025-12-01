package com.supvz.notifications_service.service.impl;

import com.supvz.notifications_service.core.exception.NotificationConflictException;
import com.supvz.notifications_service.core.exception.NotificationIsNotSentException;
import com.supvz.notifications_service.service.InboxProcessor;
import com.supvz.notifications_service.service.InboxService;
import com.supvz.notifications_service.model.entity.InboxEventType;
import com.supvz.notifications_service.service.NotificationService;
import lombok.RequiredArgsConstructor;
import lombok.extern.slf4j.Slf4j;
import org.springframework.stereotype.Service;

import java.util.UUID;

@Slf4j
@Service
@RequiredArgsConstructor
public class InboxNotificationProcessor implements InboxProcessor {
    private final InboxService inboxService;
    private final NotificationService notificationService;

    @Override
    public void process(UUID eventId) {
        log.debug("Process notification event [{}].", eventId);
        try {
            notificationService.processByEventId(eventId);
            inboxService.setProcessed(eventId);
            log.info("Notification event [{}] is processed.", eventId);
        } catch (NotificationConflictException ex) {
            log.warn("Conflict: {}", ex.getMessage());
            inboxService.setProcessed(eventId);
        } catch (NotificationIsNotSentException ex) {
            log.warn("Couldn't successfully process notification by event [{}].", eventId, ex);
            inboxService.setCleanAfter(eventId);
        } catch (RuntimeException ex) {
            log.error("Unexpected runtime exception while processing notification by event [{}].", eventId, ex);
            inboxService.setCleanAfter(eventId);
        }
    }

    @Override
    public InboxEventType getType() {
        return InboxEventType.notification;
    }
}