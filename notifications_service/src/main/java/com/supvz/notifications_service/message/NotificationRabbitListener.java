package com.supvz.notifications_service.message;

import com.fasterxml.jackson.databind.ObjectMapper;
import com.supvz.notifications_service.core.exception.InboxEventConflictException;
import com.supvz.notifications_service.core.exception.InvalidMessagePatternException;
import com.supvz.notifications_service.model.dto.InboxEventPayload;
import com.supvz.notifications_service.service.EventProcessingService;
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
    private final EventProcessingService processingService;

    @Override
    @RabbitListener(queues = "${app.messaging.notifications_queue}")
    public void listen(String message) {
        log.debug("Listened raw message: [{}]", message);
//        todo: опасный лог.
        try {
            InboxEventPayload inboxEventPayload = objectMapper.readValue(message, InboxEventPayload.class);
//            todo:  подумать про десереализацию энама. чтобы вместо ошибки налл ставился. Или вернуть ошибку, но без падения listener.
            processingService.initNotification(inboxEventPayload);
//            todo: узкое горлышко: снизу нейросетка описала это так:
//            ⚠️ Большой архитектурный нюанс:
//
//              Если initNotification вызывает логику inbox/outbox (по вашему предыдущему коду), то:
//
//              это CPU-heavy работа
//
//              listener блокируется
//
//              throughput падает
//
//              Лучше использовать:
//
//              ✔️ Listener only → push to internal queue → worker processes events
//
//              Или как минимум:
//
//              ✔️ Добавить @Async
//              ✔️ Или использовать Executor в RabbitListener контейнере
            log.info("Message [{}] is successfully listened.", inboxEventPayload.eventId());
        } catch (IOException e) {
            log.error("Failed to deserialize message [{}]: {}", message, e.getMessage());
//            todo: ну тоже лог не очень.
            throw new InvalidMessagePatternException(e.getMessage());
        } catch (InvalidMessagePatternException e) {
            log.error("Invalid message pattern: {}.", e.getMessage());
//            todo: блок возможно бесполезен
            throw e;
        } catch (InboxEventConflictException e) {
            log.info("Inbox event conflict: {}", e.getMessage());
        }
    }
}