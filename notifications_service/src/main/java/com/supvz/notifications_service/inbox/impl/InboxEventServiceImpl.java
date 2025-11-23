package com.supvz.notifications_service.inbox.impl;

import com.supvz.notifications_service.core.exception.InboxEventConflictException;
import com.supvz.notifications_service.core.exception.InboxEventNotFoundException;
import com.supvz.notifications_service.model.dto.InboxEventPayload;
import com.supvz.notifications_service.model.entity.InboxEvent;
import com.supvz.notifications_service.inbox.InboxEventService;
import com.supvz.notifications_service.inbox.InboxEventMapper;
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
public class InboxEventServiceImpl implements InboxEventService {
    private final InboxEventMapper mapper;
    private final InboxEventRepository repo;
    @Value("${app.inbox.reservation-min}")
    private int reservationInMinutes;

    @Override
    @Transactional
    public InboxEvent create(InboxEventPayload inboxEventPayload) {
        log.debug("Create inbox event [{}].", inboxEventPayload.eventId());
        InboxEvent mapped = mapper.create(inboxEventPayload);
        List<UUID> result = repo.saveIfNotExists(
                mapped.getEventId(),
                mapped.getEventType().name(),
                mapped.getPayload(),
                mapped.getCreatedAt()
        );
        if (result.isEmpty()) {
//            todo: возможно, стоит возвращать существующую сущность.
            throw new InboxEventConflictException
                    ("Inbox event [%s] is already exists.".formatted(inboxEventPayload.eventId()));
        }
        log.info("Inbox event [{}] is created.", inboxEventPayload.eventId());
        return repo.findById(inboxEventPayload.eventId()).orElseThrow();
//        todo: подумать, как сохранить и отдать за одну строку. два запроса делается. проблема производительности
    }

    @Override
    public List<UUID> readAndReserveUnprocessedBatch(int batchSize) {
        LocalDateTime reservedTo = LocalDateTime.now().plusMinutes(reservationInMinutes);
        return repo.findAndReserveUnprocessedInBatch(batchSize, reservedTo);
    }

    @Transactional
    public void reserveEvent(InboxEvent event) {
//        todo: batched reserve надо
        LocalDateTime reservedTo = LocalDateTime.now().plusMinutes(reservationInMinutes);
        int i = repo.reserve(event, reservedTo);

        if (i == 0) {
            log.debug("Inbox event [{}] is already reserved.", event.getEventId());
            return;
        }
        log.info("Inbox event [{}] reserved to {}.", event.getEventId(), reservedTo);
    }

    @Override
    @Transactional
    public void markProcessed(InboxEvent event, LocalDateTime processedAt) {
        log.debug("Marking event [{}] as processed.", event.getEventId());

        event.setProcessedAt(processedAt);
        event.setProcessed(true);
//        todo: жестко подумать про конкуренцию и проверку, зарезервирован ли.

        repo.save(event);

        log.debug("Event [{}] is marked as processed.", event.getEventId());
    }

    @Override
    public InboxEvent getById(UUID eventId) {
        return repo.findById(eventId)
                .orElseThrow(() -> new InboxEventNotFoundException("Inbox event [%s] was not found."
                        .formatted(eventId)));
    }
}
