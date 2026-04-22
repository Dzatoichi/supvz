package com.supvz.notifications_service.mapper;

import com.supvz.notifications_service.model.dto.InboxMessage;
import com.supvz.notifications_service.model.entity.InboxEvent;
import lombok.extern.slf4j.Slf4j;
import org.springframework.stereotype.Component;

import java.time.LocalDateTime;

/**
 * <h3>
 * Маппер для обработки inbox событий.
 * </h3>
 */
@Slf4j
@Component
public class InboxEntityMapper implements InboxMapper {

    /**
     * Маппинг сообщения в сущность.
     * @param message - сообщение, полученное из очереди.
     * @return InboxEvent - сущность для последующего сохранения в БД.
     */
    @Override
    public InboxEvent create(InboxMessage message) {
            return InboxEvent.builder()
                    .eventId(message.eventId())
                    .eventType(message.eventType())
                    .payload(message.payload())
                    .build();
    }

    /**
     * <h4>
     * Маркировка события как обработанного.
     * </h4>
     * Также очищает поля clean_after и reserved_to.
     *
     * @param event сущность события.
     */
    @Override
    public void markAsProcessed(InboxEvent event) {
        event.setProcessedAt(LocalDateTime.now());
        event.setProcessed(true);
        event.setReservedTo(null);
        event.setCleanAfter(null);
    }

    /**
     * <h4>
     * Установка "таймера" для очистки в случае ошибки обработки события.
     * </h4>
     * <br/>
     * Но вплоть до конца этого таймера событие продолжает обрабатываться в случае ошибки со стороны клиентов-сервисов или вообще сервера.
     *
     * @param event сущность события.
     * @param cleanAfter время, после которого событие можно удалять.
     */
    @Override
    public void setCleanAfter(InboxEvent event, LocalDateTime cleanAfter) {
        event.setCleanAfter(cleanAfter);
        event.setReservedTo(null);
    }
}