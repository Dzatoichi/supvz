package com.supvz.notifications_service.message;

import com.fasterxml.jackson.core.JsonProcessingException;
import com.fasterxml.jackson.databind.ObjectMapper;
import com.supvz.notifications_service.core.MessageDto;
import com.supvz.notifications_service.entity.InboxEvent;
import com.supvz.notifications_service.entity.Notification;
import com.supvz.notifications_service.inbox.InboxEventService;
import com.supvz.notifications_service.service.NotificationService;
import lombok.RequiredArgsConstructor;
import lombok.extern.slf4j.Slf4j;
import org.springframework.stereotype.Service;
import org.springframework.transaction.annotation.Transactional;

@Slf4j
@Service
@RequiredArgsConstructor
public class MessageConsumerImpl implements MessageConsumer {
    private final ObjectMapper objectMapper;
    private final InboxEventService inboxEventService;
    private final NotificationService notificationService;

    @Override
    @Transactional
    public void consume(String message) {
        log.info("CONSUME MESSAGE [{}].", message);
        try {
            MessageDto messageDto = objectMapper.readValue(message, MessageDto.class);
            InboxEvent event = inboxEventService.create(messageDto);
            Notification notification = notificationService.create(event);
            log.info("NOTIFICATION [{}] IS SUCCESSFULLY CREATED.", notification.getId());
        } catch (JsonProcessingException e) {
            log.warn("ERROR CONSUMING MESSAGE: {}",  e.getMessage());
        }
        log.info("CONSUMING IS ENDED.");
    }
}
