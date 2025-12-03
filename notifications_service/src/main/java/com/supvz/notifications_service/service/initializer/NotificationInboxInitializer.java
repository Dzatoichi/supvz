package com.supvz.notifications_service.service.initializer;

import com.fasterxml.jackson.core.JsonProcessingException;
import com.fasterxml.jackson.databind.ObjectMapper;
import com.supvz.notifications_service.model.dto.InboxMessage;
import com.supvz.notifications_service.model.dto.NotificationPayload;
import com.supvz.notifications_service.model.entity.InboxEvent;
import com.supvz.notifications_service.model.entity.InboxEventType;
import com.supvz.notifications_service.service.entity.InboxService;
import com.supvz.notifications_service.service.entity.NotificationService;
import lombok.RequiredArgsConstructor;
import lombok.extern.slf4j.Slf4j;
import org.springframework.stereotype.Service;
import org.springframework.transaction.annotation.Transactional;

/**
 * <h3>
 * Инициализатор - слой между слушателем и сервисами для создания сущностей Inbox и Notification.
 * </h3>
 * Следует паттерну Strategy.
 */
@Slf4j
@Service
@RequiredArgsConstructor
public class NotificationInboxInitializer implements InboxInitializer {
    private final InboxService inboxService;
    private final NotificationService notificationService;
    private final ObjectMapper objectMapper;

    /**
     * Инициализация события и его сущности нотификации.
     *
     * @param inbox сообщение, полученное из очереди.
     * @throws JsonProcessingException исключение при неправильной модели полезной нагрузки нотификации.
     */
    @Override
    @Transactional
    public void initialize(InboxMessage inbox) throws JsonProcessingException {
        log.debug("Инициализация события нотификации: [{}].", inbox.eventId());
        NotificationPayload payload = objectMapper.readValue(inbox.payload(), NotificationPayload.class);
        InboxEvent inboxEvent = inboxService.create(inbox);
        notificationService.create(inboxEvent, payload);
        log.info("Событие нотификации [{}] инициализировано.", inbox.eventId());
    }

    /**
     * Метод для реализации паттерна Strategy.
     *
     * @return InboxEventType - тип события, с которым работает инициализатор.
     */
    @Override
    public InboxEventType getType() {
        return InboxEventType.notification;
    }
}