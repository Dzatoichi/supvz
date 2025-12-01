package com.supvz.notifications_service.service.impl;

import com.supvz.notifications_service.core.exception.InboxEventConflictException;
import com.supvz.notifications_service.core.exception.InboxEventNotFoundException;
import com.supvz.notifications_service.model.dto.InboxMessage;
import com.supvz.notifications_service.model.entity.EventIdTypeProjection;
import com.supvz.notifications_service.model.entity.InboxEvent;
import com.supvz.notifications_service.service.InboxService;
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

    @Override
    @Transactional
    public InboxEvent create(InboxMessage inboxMessage) {
        log.debug("Create inbox event [{}].", inboxMessage.eventId());
        InboxEvent mapped = mapper.create(inboxMessage);
        log.debug("mapped event type obj: {}. class: {}", mapped.getEventType(), mapped.getEventType().getClass());
        InboxEvent created = repo.saveIfNotExists(
                mapped.getEventId(),
                mapped.getEventType().name(),
                mapped.getPayload());
        if (created == null) {
            throw new InboxEventConflictException
                    ("Inbox event [%s] is already exists.".formatted(inboxMessage.eventId()));
        }
        log.info("Inbox event [{}] is created.", inboxMessage.eventId());
        return created;
    }

    @Override
    public List<EventIdTypeProjection> readAndReserveUnprocessedBatch(int batchSize) {
        LocalDateTime reservedTo = LocalDateTime.now().plusMinutes(reservationInMinutes);
        return repo.findAndReserveUnprocessedInBatch(batchSize, reservedTo);
    }

    @Override
    @Transactional
    public void setProcessed(UUID eventId) {
        log.debug("Marking event [{}] as processed.", eventId);
        InboxEvent event = repo.findById(eventId)
                .orElseThrow(() -> new InboxEventNotFoundException("Inbox event [%s] was not found."
                        .formatted(eventId)));
        if (event.getProcessed()) {
            log.debug("Event [{}] already marked as processed.", event.getEventId());
            return;
        }
        mapper.markAsProcessed(event);
        repo.save(event);
        log.debug("Event [{}] is marked as processed.", event.getEventId());
    }

    @Override
    @Transactional
    public void setCleanAfter(UUID eventId) {
        log.debug("Marking event [{}] as failed.", eventId);
        InboxEvent event = repo.findById(eventId)
                .orElseThrow(() -> new InboxEventNotFoundException("Inbox event [%s] was not found."
                        .formatted(eventId)));
        if (event.getCleanAfter() != null) {
            log.debug("Event [{}] already marked as failed.", event.getEventId());
            return;
        }
        LocalDateTime cleanAfter = LocalDateTime.now().plusMinutes(cleaningInMinutes);
        mapper.setCleanAfter(event, cleanAfter);
        repo.save(event);
        log.debug("Event [{}] is marked as failed.", event.getEventId());
    }

    @Override
    public List<UUID> deleteFailedBatch(Integer batchSize) {
        return repo.deleteFailedInBatch(batchSize);
    }
}