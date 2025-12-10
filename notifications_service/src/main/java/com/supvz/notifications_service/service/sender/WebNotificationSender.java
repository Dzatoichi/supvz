package com.supvz.notifications_service.service.sender;

import com.fasterxml.jackson.core.JsonProcessingException;
import com.fasterxml.jackson.databind.ObjectMapper;
import com.supvz.notifications_service.core.exception.NotificationNotSerializedException;
import com.supvz.notifications_service.model.dto.NotificationDto;
import com.supvz.notifications_service.model.entity.NotificationType;
import lombok.RequiredArgsConstructor;
import lombok.extern.slf4j.Slf4j;
import org.springframework.beans.factory.annotation.Value;
import org.springframework.messaging.MessagingException;
import org.springframework.messaging.simp.SimpMessagingTemplate;
import org.springframework.stereotype.Service;
import org.springframework.transaction.annotation.Propagation;
import org.springframework.transaction.annotation.Transactional;

import java.net.URLEncoder;
import java.nio.charset.StandardCharsets;

/**
 * <h3>
 * Реализация процессора для обработки нотификаций типа web.
 * </h3>
 * Следует паттерну Strategy.
 * <br/>
 * <br/>
 * Данный тип нотификаций предназначен для отправки по веб-сокету.
 */
@Slf4j
@Service
@RequiredArgsConstructor
public class WebNotificationSender implements NotificationSender {
    private final SimpMessagingTemplate messagingTemplate;
    private final ObjectMapper objectMapper;
    @Value("${app.websocket.base-topic}")
    private String baseTopic;

    /**
     * Метод отправки нотификации подключенному клиенту через веб-сокет.
     *
     * @param notification ДТО нотификации.
     */
    @Override
    @Transactional(propagation = Propagation.NOT_SUPPORTED)
    public void send(NotificationDto notification) {
        String destination = getDestination(notification);
        log.debug("Отправка 'web' нотификации [{}]. Получатель [{}].", notification.id(), destination);
        try {
            messagingTemplate.convertAndSend(destination, objectMapper.writeValueAsString(notification));
            log.info("Нотификация 'web' успешно [{}] отправлена.", notification.id());
        } catch (MessagingException ex) {
            log.error("Не получилось отправить 'web' нотификацию [{}].", notification.id());
            throw ex;
        } catch (JsonProcessingException ex) {
            log.error("Не получить сериализовать нотификаций [{}] в json.", notification.id());
            throw new NotificationNotSerializedException(ex.getMessage());
        }
    }

    /**
     * Метод для реализации паттерна Strategy.
     *
     * @return NotificationType - тип нотификации, с которым работает процессор.
     */
    @Override
    public NotificationType getType() {
        return NotificationType.web;
    }

    private String getDestination(NotificationDto notification) {
        String recipient = URLEncoder.encode(notification.recipientId(), StandardCharsets.UTF_8);
        return "/".concat(baseTopic).concat("/").concat(recipient);
    }
}