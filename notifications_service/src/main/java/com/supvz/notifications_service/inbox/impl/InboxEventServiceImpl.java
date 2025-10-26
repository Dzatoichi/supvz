package com.supvz.notifications_service.inbox.impl;

import com.supvz.notifications_service.core.exception.InboxEventConflictException;
import com.supvz.notifications_service.core.dto.MessageDto;
import com.supvz.notifications_service.entity.InboxEvent;
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

    @Value("${inbox.reservation_in_minutes}")
    private int reservationMinutes;

    @Override
    @Transactional
    public InboxEvent create(MessageDto messageDto) {
        log.debug("Create inbox event [{}].", messageDto.eventId());
        InboxEvent mapped = mapper.create(messageDto);
        List<UUID> result = repo.saveIfNotExists(
                mapped.getEventId(),
                mapped.getEventType().name(),
                mapped.getPayload(),
                mapped.getCreatedAt()
        );
        if (result.isEmpty()) {
            throw new InboxEventConflictException
                    ("Inbox event [%s] is already exists.".formatted(messageDto.eventId()));
        }
        log.info("Inbox event [{}] is created.", messageDto.eventId());
        return repo.findById(messageDto.eventId()).orElseThrow();
    }

    @Override
    public List<InboxEvent> readFirstUnprocessed(int firstNumber) {
        return repo.findAllUnprocessed(firstNumber);
    }

    @Transactional
    public void reserveEvent(InboxEvent event) {
        LocalDateTime reservedTo = LocalDateTime.now().plusMinutes(reservationMinutes);
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

        repo.save(event);

        log.debug("Event [{}] is marked as processed.", event.getEventId());
    }
}
