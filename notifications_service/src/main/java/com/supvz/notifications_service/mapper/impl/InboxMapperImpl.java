package com.supvz.notifications_service.mapper.impl;

import com.fasterxml.jackson.core.JsonProcessingException;
import com.fasterxml.jackson.databind.ObjectMapper;
import com.supvz.notifications_service.core.exception.InboxEventNotSerializedException;
import com.supvz.notifications_service.model.dto.InboxMessage;
import com.supvz.notifications_service.model.entity.InboxEvent;
import com.supvz.notifications_service.mapper.InboxMapper;
import lombok.RequiredArgsConstructor;
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
@RequiredArgsConstructor
public class InboxMapperImpl implements InboxMapper {
    private final ObjectMapper objectMapper;

    /**
     * Маппинг сообщения в сущность.
     * @param event - сообщение, полученное из очереди.
     * @return InboxEvent - сущность для последующего сохранения в БД.
     */
    @Override
    public InboxEvent create(InboxMessage event) {
        try {
            return InboxEvent.builder()
                    .eventId(event.eventId())
                    .eventType(event.eventType())
                    .payload(objectMapper.writeValueAsString(event.payload()))
                    .build();
        } catch (JsonProcessingException ex) {
            log.error("Couldn't serialize payload of event [{}].", event.eventId());
            throw new InboxEventNotSerializedException(ex.getMessage());
        }
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