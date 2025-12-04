package com.supvz.notifications_service.service.entity;

import com.supvz.notifications_service.core.exception.InboxEventConflictException;
import com.supvz.notifications_service.core.exception.InboxEventNotFoundException;
import com.supvz.notifications_service.model.dto.InboxMessage;
import com.supvz.notifications_service.model.entity.EventIdTypeProjection;
import com.supvz.notifications_service.model.entity.InboxEvent;
import com.supvz.notifications_service.mapper.InboxMapper;
import com.supvz.notifications_service.repo.InboxEventRepository;
import lombok.RequiredArgsConstructor;
import lombok.extern.slf4j.Slf4j;
import org.springframework.beans.factory.annotation.Value;
import org.springframework.stereotype.Service;
import org.springframework.transaction.annotation.Transactional;

import java.time.LocalDateTime;
import java.util.List;
import java.util.UUID;

/**
 * <h3>
 * Реализация сервиса для обработки сущностей Inbox.
 * </h3>
 */
@Slf4j
@Service
@RequiredArgsConstructor
public class InboxEntityService implements InboxService {
    private final InboxMapper mapper;
    private final InboxEventRepository repo;
    @Value("${app.inbox.reservation-min}")
    private int reservationInMinutes;
    @Value("${app.inbox.cleaning-min}")
    private int cleaningInMinutes;

    /**
     * Маппинг сообщения в сущность.
     *
     * @param inboxMessage полученное сообщение из очереди.
     * @return InboxEvent - сущность inbox события.
     */
    @Override
    @Transactional
    public InboxEvent create(InboxMessage inboxMessage) {
        log.debug("Создание сущности inbox события [{}].", inboxMessage.eventId());
        InboxEvent mapped = mapper.create(inboxMessage);
        InboxEvent created = repo.saveIfNotExists(
                mapped.getEventId(),
                mapped.getEventType().name(),
                mapped.getPayload());
        if (created == null) {
            throw new InboxEventConflictException
                    ("Inbox событие [%s] уже существует.".formatted(inboxMessage.eventId()));
        }
        log.info("Сущность inbox события [{}] создана.", inboxMessage.eventId());
        return created;
    }

    /**
     * Реализация получения и резервации батча событий в одной транзакции.
     *
     * @param batchSize задает размер батча.
     * @return список зарезервированных необработанных событий.
     */
    @Override
    public List<EventIdTypeProjection> readAndReserveUnprocessedBatch(int batchSize) {
        LocalDateTime reservedTo = LocalDateTime.now().plusMinutes(reservationInMinutes);
        return repo.findAndReserveUnprocessedInBatch(batchSize, reservedTo);
    }

    /**
     * Маркировка события как обработанного.
     *
     * @param eventId идентификатор события.
     */
    @Override
    @Transactional
    public void setProcessed(UUID eventId) {
        log.debug("Отметка inbox события [{}] как обработанного.", eventId);
        InboxEvent event = repo.findById(eventId)
                .orElseThrow(() -> new InboxEventNotFoundException("Inbox событие [%s] не найдено."
                        .formatted(eventId)));
        if (event.getProcessed()) {
            log.debug("Inbox событие [{}] уже отмечено как обработанное.", event.getEventId());
            return;
        }
        mapper.markAsProcessed(event);
        repo.save(event);
        log.debug("Inbox событие [{}] успешно отмечено как обработанное..", event.getEventId());
    }

    /**
     * Установка таймера для удаления события в случае ошибки обработки.
     *
     * @param eventId идентификатор события.
     */
    @Override
    @Transactional
    public void setCleanAfter(UUID eventId) {
        log.debug("Отметка inbox события [{}] для очистки.", eventId);
        InboxEvent event = repo.findById(eventId)
                .orElseThrow(() -> new InboxEventNotFoundException("Inbox событие [%s] не найдено."
                        .formatted(eventId)));
        if (event.getCleanAfter() != null) {
            log.debug("Inbox событие [{}] уже отмечено для очистки.", eventId);
            return;
        }
        LocalDateTime cleanAfter = LocalDateTime.now().plusMinutes(cleaningInMinutes);
        mapper.setCleanAfter(event, cleanAfter);
        repo.save(event);
        log.debug("Отметка inbox события [{}] выполнена.", event.getEventId());
    }

    /**
     * Удаление батча событий, у которых прошел таймер удаления.
     *
     * @param batchSize размер батча для удаления событий.
     * @return List - список удаленных событий.
     */
    @Override
    public List<UUID> deleteFailedBatch(Integer batchSize) {
        return repo.deleteFailedInBatch(batchSize);
    }
}