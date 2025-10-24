package com.supvz.notifications_service.message;

import com.fasterxml.jackson.databind.ObjectMapper;
import com.supvz.notifications_service.core.exception.InboxEventConflictException;
import com.supvz.notifications_service.core.exception.InvalidMessagePatternException;
import com.supvz.notifications_service.core.dto.MessageDto;
import com.supvz.notifications_service.service.MessageProcessingService;
import lombok.RequiredArgsConstructor;
import lombok.extern.slf4j.Slf4j;
import org.springframework.amqp.rabbit.annotation.RabbitListener;
import org.springframework.stereotype.Component;

import java.io.IOException;

@Slf4j
@Component
@RequiredArgsConstructor
public class NotificationRabbitListener implements MessageListener {
    private final ObjectMapper objectMapper;
    private final MessageProcessingService processingService;

    @Override
    @RabbitListener(queues = {"${messaging.notifications_queue}"})
    public void listen(String message) {
        log.info("Listened raw message: [{}]", message);
        try {
            MessageDto messageDto = objectMapper.readValue(message, MessageDto.class);
            processingService.initNotification(messageDto);
            log.info("Message [{}] is successfully processed.", messageDto.eventId());
        } catch (IOException e) {
            log.error("Failed to deserialize message [{}]: {}", message, e.getMessage());
            throw new InvalidMessagePatternException(e.getMessage());
        } catch (InvalidMessagePatternException e) {
            log.error("Invalid message pattern: {}.", e.getMessage());
            throw e;
        } catch (InboxEventConflictException e) {
            log.info("Inbox event conflict: {}", e.getMessage());
        }
    }
}