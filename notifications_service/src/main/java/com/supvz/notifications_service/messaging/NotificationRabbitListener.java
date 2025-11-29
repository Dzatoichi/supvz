package com.supvz.notifications_service.messaging;

import com.supvz.notifications_service.core.exception.InboxEventConflictException;
import com.supvz.notifications_service.model.dto.InboxEventMessage;
import com.supvz.notifications_service.model.dto.NotificationPayload;
import com.supvz.notifications_service.service.EventProcessor;
import jakarta.validation.Valid;
import lombok.RequiredArgsConstructor;
import lombok.extern.slf4j.Slf4j;
import org.springframework.amqp.rabbit.annotation.RabbitListener;
import org.springframework.messaging.handler.annotation.Payload;
import org.springframework.stereotype.Component;

@Slf4j
@Component
@RequiredArgsConstructor
public class NotificationRabbitListener {
    private final EventProcessor processingService;

    @RabbitListener(queues = "${app.messaging.inbox-queue}")
    public void listen(@Payload @Valid InboxEventMessage inboxEvent) {
        log.debug("Listened inbox event [{}].", inboxEvent.eventId());
        try {
            switch (inboxEvent.eventType()) {
                case notification -> {
                    NotificationPayload payload = (NotificationPayload) inboxEvent.payload();
                    processingService.initNotification(inboxEvent, payload);
                }
                case other -> processingService.initOther(inboxEvent);
                default -> log.warn("Unhandled event type [{}], ignoring event [{}].",
                        inboxEvent.eventType(), inboxEvent.eventId());
            }
            log.info("Event [{}] is successfully listened.", inboxEvent.eventId());
        } catch (InboxEventConflictException e) {
            log.warn("Inbox event conflict: {}", e.getMessage(), e);
        }
    }
}