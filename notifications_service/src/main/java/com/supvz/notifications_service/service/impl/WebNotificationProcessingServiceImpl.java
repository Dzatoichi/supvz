package com.supvz.notifications_service.service.impl;

import com.supvz.notifications_service.model.entity.Notification;
import com.supvz.notifications_service.service.WebNotificationProcessingService;
import lombok.RequiredArgsConstructor;
import lombok.extern.slf4j.Slf4j;
import org.springframework.beans.factory.annotation.Value;
import org.springframework.messaging.MessagingException;
import org.springframework.messaging.simp.SimpMessagingTemplate;
import org.springframework.stereotype.Service;

import java.util.Map;

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
    @Value("${app.websocket.base-topic}")
    private String baseTopic;

    /**
     * Реализация отправки уведомления подключенному клиенту через веб-сокет.
     */
    @Override
    public void send(Notification notification) {
        String destination = "/".concat(baseTopic).concat("/").concat(notification.getSubject());
//        todo: переосмыслить создание пути. этот способ небезопасен
        log.debug("Sending web notification [{}] to destination [{}].", notification.getId(), destination);
        try {
            Map<String, Object> message = Map.of("body", notification.getBody());
//            todo: почему только тело? подумать про другие поля.
            messagingTemplate.convertAndSend(destination, message);
//            todo: а что если не получилось? подумать про компенсирующее действие, ретрай.
            log.info("Web notification [{}] is sent.", notification.getId());
        } catch (MessagingException e) {
            log.error("Couldn't send web notification [{}]: {}.", notification.getId(), e.getMessage());
            throw e;
        }
    }
}
