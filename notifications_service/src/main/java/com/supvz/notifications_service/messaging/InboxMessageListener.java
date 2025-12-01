package com.supvz.notifications_service.messaging;

import com.fasterxml.jackson.databind.ObjectMapper;
import com.supvz.notifications_service.core.exception.InboxEventConflictException;
import com.supvz.notifications_service.core.exception.InboxEventNotSerializedException;
import com.supvz.notifications_service.service.InboxInitializer;
import com.supvz.notifications_service.model.dto.InboxMessage;
import com.supvz.notifications_service.model.entity.InboxEventType;
import lombok.extern.slf4j.Slf4j;
import org.springframework.amqp.core.Message;
import org.springframework.amqp.rabbit.annotation.RabbitListener;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.stereotype.Component;

import java.io.IOException;
import java.util.List;
import java.util.Map;
import java.util.function.Function;
import java.util.stream.Collectors;

@Slf4j
@Component
public class InboxMessageListener {
    private final ObjectMapper objectMapper;
    private final Map<InboxEventType, InboxInitializer> initializers;

    @Autowired
    public InboxMessageListener(
            ObjectMapper objectMapper,
            List<InboxInitializer> initializerList
    ) {
        this.objectMapper = objectMapper;
        this.initializers = initializerList.stream()
                .collect(Collectors.toMap(InboxInitializer::getType, Function.identity()));
    }

    @RabbitListener(queues = "${app.messaging.inbox-queue}")
    public void listen(Message message) {
        try {
            InboxMessage inboxEvent = objectMapper.readValue(message.getBody(), InboxMessage.class);
            log.debug("Listened inbox event [{}].", inboxEvent.eventId());
            try {
                initializers.get(inboxEvent.eventType()).initialize(inboxEvent);
            } catch (NullPointerException ex) {
                log.warn("Unhandled event type [{}], ignoring event [{}].",
                        inboxEvent.eventType(), inboxEvent.eventId());
                return;
            }
            log.info("Event [{}] is successfully listened.", inboxEvent.eventId());
        } catch (IOException ex) {
            log.error("Couldn't serialize inbox event.", ex);
            throw new InboxEventNotSerializedException(ex.getMessage());
        } catch (InboxEventConflictException ex) {
            log.warn("Inbox event conflict: [{}]", ex.getMessage());
        }
    }
}