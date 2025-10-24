package com.supvz.notifications_service.service.impl;

import com.supvz.notifications_service.entity.InboxEvent;
import com.supvz.notifications_service.entity.Notification;
import com.supvz.notifications_service.mapper.NotificationMapper;
import com.supvz.notifications_service.repo.NotificationRepository;
import com.supvz.notifications_service.service.MessageProcessingService;
import com.supvz.notifications_service.service.NotificationService;
import lombok.RequiredArgsConstructor;
import lombok.extern.slf4j.Slf4j;
import org.springframework.stereotype.Service;
import org.springframework.transaction.annotation.Transactional;

import java.util.UUID;

@Slf4j
@Service
@RequiredArgsConstructor
public class NotificationServiceImpl implements NotificationService {
    private final NotificationMapper mapper;
    private final NotificationRepository repo;

    @Override
    @Transactional
    public void create(InboxEvent event) {
        log.info("Create notification by type [{}], by event [{}].", event.getEventType(), event.getEventId());

        Notification mapped = mapper.create(event);

        Notification saved = repo.save(mapped);

        log.info("Notification [{}] by event [{}] is created.", saved.getId(), event.getEventId());
    }

    @Override
    public Notification findByEventId(UUID eventId) {
        log.info("Get notification by event [{}].", eventId);
        //todo exception

        return repo.findByEventId(eventId)
                .orElseThrow();
    }
}
