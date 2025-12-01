package com.supvz.notifications_service.service.impl;

import com.fasterxml.jackson.core.JsonProcessingException;
import com.fasterxml.jackson.databind.ObjectMapper;
import com.supvz.notifications_service.core.exception.NotificationNotSerializedException;
import com.supvz.notifications_service.model.dto.NotificationDto;
import com.supvz.notifications_service.model.entity.NotificationType;
import com.supvz.notifications_service.service.NotificationProcessor;
import lombok.RequiredArgsConstructor;
import lombok.extern.slf4j.Slf4j;
import org.springframework.beans.factory.annotation.Value;
import org.springframework.messaging.MessagingException;
import org.springframework.messaging.simp.SimpMessagingTemplate;
import org.springframework.retry.annotation.Retryable;
import org.springframework.stereotype.Service;
import org.springframework.transaction.annotation.Propagation;
import org.springframework.transaction.annotation.Transactional;

import java.net.URLEncoder;
import java.nio.charset.StandardCharsets;

/**
 * <h3>
 * Реализация сервиса для отправки веб-сокет уведомлений.
 * </h3>
 */
@Slf4j
@Service
@RequiredArgsConstructor
public class WebNotificationProcessor implements NotificationProcessor {
    private final SimpMessagingTemplate messagingTemplate;
    private final ObjectMapper objectMapper;
    @Value("${app.websocket.base-topic}")
    private String baseTopic;

    /**
     * Реализация отправки уведомления подключенному клиенту через веб-сокет.
     */
    @Override
//    @Retryable(retryFor = MessagingException.class, maxAttemptsExpression = "${app.notification.number-retry-attempts}")
    @Transactional(propagation = Propagation.NOT_SUPPORTED)
    public void send(NotificationDto notification) {
        String destination = getDestination(notification);
        log.debug("Sending web notification [{}] to destination [{}].", notification.id(), destination);
        try {
            messagingTemplate.convertAndSend(destination, objectMapper.writeValueAsString(notification));
            log.info("Web notification [{}] is sent.", notification.id());
        } catch (MessagingException ex) {
            log.error("Couldn't send web notification [{}]: {}.", notification.id(), ex.getMessage());
            throw ex;
        } catch (JsonProcessingException ex) {
            log.error("Couldn't serialize notification [{}] to json.", notification.id(), ex);
            throw new NotificationNotSerializedException(ex.getMessage());
        }
    }

    @Override
    public NotificationType getType() {
        return NotificationType.web;
    }

    private String getDestination(NotificationDto notification) {
        String recipient = URLEncoder.encode(notification.recipientId(), StandardCharsets.UTF_8);
        return "/".concat(baseTopic).concat("/").concat(recipient);
    }
}
