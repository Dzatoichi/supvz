package com.supvz.notifications_service.messaging;

import com.fasterxml.jackson.databind.ObjectMapper;
import com.supvz.notifications_service.core.exception.InboxEventConflictException;
import com.supvz.notifications_service.model.dto.InboxEventPayload;
import com.supvz.notifications_service.model.dto.NotificationPayload;
import com.supvz.notifications_service.service.EventProcessingService;
import lombok.RequiredArgsConstructor;
import lombok.extern.slf4j.Slf4j;
import org.springframework.amqp.core.Message;
import org.springframework.amqp.rabbit.annotation.RabbitListener;
import org.springframework.stereotype.Component;

import java.io.IOException;

@Slf4j
@Component
@RequiredArgsConstructor
public class NotificationRabbitListener {
    private final ObjectMapper objectMapper;
    private final EventProcessingService processingService;

    @RabbitListener(queues = "${app.messaging.inbox-queue}")
    public void listen(Message message) {
        log.debug("Listened raw message, size: [{}]", message.getBody().length);
        try {
            InboxEventPayload inboxEventPayload = objectMapper
                    .readValue(message.getBody(), InboxEventPayload.class);
            switch (inboxEventPayload.eventType()) {
                case notification -> {
                    NotificationPayload notificationPayload = objectMapper
                            .readValue(inboxEventPayload.payload(), NotificationPayload.class);
                    processingService.initNotification(inboxEventPayload, notificationPayload);
                }
                case other -> processingService.initOther(inboxEventPayload);
                default -> log.warn("Unhandled event type [{}], ignoring event [{}].",
                        inboxEventPayload.eventType(), inboxEventPayload.eventId());
            }
            log.info("Event [{}] is successfully listened.", inboxEventPayload.eventId());
        } catch (IOException e) {
            log.error("Failed to deserialize message, size: [{}]", message.getBody().length, e);
        } catch (InboxEventConflictException e) {
            log.warn("Inbox event conflict: {}", e.getMessage(), e);
        }
    }
}