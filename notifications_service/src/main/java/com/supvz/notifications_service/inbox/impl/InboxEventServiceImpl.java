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
import org.springframework.dao.DataIntegrityViolationException;
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
        log.info("Create inbox event [{}].", messageDto.eventId());
        try {
            InboxEvent mapped = mapper.create(messageDto);
            InboxEvent saved = repo.save(mapped);
            log.info("Inbox event [{}] is created.", saved.getEventId());
            return saved;
        } catch (DataIntegrityViolationException e) {
            throw new InboxEventConflictException
                    ("Inbox event [%s] is already exists.".formatted(messageDto.eventId()));
        }
    }

    @Override
    public List<UUID> readFirstUnprocessed(int firstNumber) {
        log.info("Read first {} unprocessed.", firstNumber);

        List<InboxEvent> events = repo.findAllUnprocessed(firstNumber);
        return reserveList(events);
    }

    @Override
    public List<UUID> reserveList(List<InboxEvent> events) {
        List<UUID> eventsIds = events.stream().map(InboxEvent::getEventId).toList();
        log.info("Reserve events {}.", eventsIds.isEmpty() ? "[EMPTY LIST]" : eventsIds);

        for (UUID id : eventsIds) {
            LocalDateTime reservedTo = LocalDateTime.now().plusMinutes(reservationMinutes);
            int i = repo.reserve(id, reservedTo);

            if (i == 0) throw new InboxEventConflictException("Inbox event [%s] is already reserved.".formatted(id));
            log.info("Inbox event [{}] reserved to {}.", id, reservedTo);
        }
        return eventsIds;
    }
}
