package com.supvz.notifications_service.service.impl;

import com.fasterxml.jackson.core.JsonProcessingException;
import com.fasterxml.jackson.databind.ObjectMapper;
import com.supvz.notifications_service.model.entity.Notification;
import com.supvz.notifications_service.service.WebNotificationProcessingService;
import lombok.RequiredArgsConstructor;
import lombok.extern.slf4j.Slf4j;
import org.springframework.beans.factory.annotation.Value;
import org.springframework.messaging.MessagingException;
import org.springframework.messaging.simp.SimpMessagingTemplate;
import org.springframework.retry.annotation.Retryable;
import org.springframework.stereotype.Service;

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
public class WebNotificationProcessingServiceImpl implements WebNotificationProcessingService {
    private final SimpMessagingTemplate messagingTemplate;
    private final ObjectMapper objectMapper;
    @Value("${app.websocket.base-topic}")
    private String baseTopic;

    /**
     * Реализация отправки уведомления подключенному клиенту через веб-сокет.
     */
    @Override
    @Retryable(retryFor = MessagingException.class, maxAttemptsExpression = "${app.notification.number-retry-attempts}")
    public void send(Notification notification) {
        String destination = getDestination(notification);
        log.debug("Sending web notification [{}] to destination [{}].", notification.getId(), destination);
        try {
            messagingTemplate.convertAndSend(destination, objectMapper.writeValueAsString(notification));
            log.info("Web notification [{}] is sent.", notification.getId());
        } catch (MessagingException e) {
            log.error("Couldn't send web notification [{}]: {}.", notification.getId(), e.getMessage());
            throw e;
        } catch (JsonProcessingException e) {
            log.error("Couldn't serialize notification [{}] to json.", notification.getId(), e);
            throw new RuntimeException(e);
        }
    }

    private String getDestination(Notification notification) {
        String recipient = URLEncoder.encode(notification.getRecipientId(), StandardCharsets.UTF_8);
        return "/".concat(baseTopic).concat("/").concat(recipient);
    }
}
