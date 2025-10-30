package com.supvz.notifications_service.service.impl;

import com.supvz.notifications_service.core.dto.NotificationDto;
import com.supvz.notifications_service.core.dto.PageDto;
import com.supvz.notifications_service.core.exception.InboxEventNotFoundException;
import com.supvz.notifications_service.core.filter.DateNotificationFilter;
import com.supvz.notifications_service.core.filter.NotificationFilter;
import com.supvz.notifications_service.entity.InboxEvent;
import com.supvz.notifications_service.entity.Notification;
import com.supvz.notifications_service.entity.NotificationType;
import com.supvz.notifications_service.mapper.NotificationMapper;
import com.supvz.notifications_service.repo.NotificationRepository;
import com.supvz.notifications_service.service.NotificationService;
import lombok.RequiredArgsConstructor;
import lombok.extern.slf4j.Slf4j;
import org.springframework.data.domain.Page;
import org.springframework.data.domain.PageRequest;
import org.springframework.data.domain.Pageable;
import org.springframework.stereotype.Service;
import org.springframework.transaction.annotation.Transactional;

import java.time.LocalDateTime;
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
        log.debug("Create notification by type [{}], by event [{}].", event.getEventType(), event.getEventId());
        Notification mapped = mapper.create(event);
        Notification saved = repo.save(mapped);
        log.info("Notification [{}] by event [{}] is created.", saved.getId(), event.getEventId());
    }

    @Override
    public Notification getByEventId(UUID eventId) {
        log.debug("Get event [{}].", eventId);
        return repo.findByEventId(eventId)
                .orElseThrow(() -> new InboxEventNotFoundException("Inbox event [%s] was not found.".formatted(eventId)));
    }

    @Override
    @Transactional
    public void markAsSent(Notification notification, LocalDateTime sentAndProcessedAt) {
        log.debug("Mark notification [{}] as sent.", notification.getId());
        notification.setSentAt(sentAndProcessedAt);
        repo.save(notification);
        log.debug("Notification [{}] is marked as sent.", notification.getId());
    }

    @Override
    public PageDto<NotificationDto> findAll(int page, int size, NotificationFilter filter) {
        log.debug("Read all. Page {}, size {}.", page, size);
//      Параметры фильтрации
        Pageable pageable = PageRequest.of(page, size);
        String recipientId = filter.recipientId();
        UUID eventId = filter.eventId();
        LocalDateTime sentAt = filter.sentAt();
        NotificationType type = filter.type();
        Boolean viewed = filter.viewed();
        DateNotificationFilter dateFilter = filter.dateFilter();
        boolean filterByDate = dateFilter != null && (dateFilter.startDate() != null & dateFilter.endDate() != null);
//      Получение странички.
        Page<Notification> notificationPage;
        if (filterByDate) {
            notificationPage = repo.findAllWithDateFilter(pageable, recipientId,
                    eventId, type, viewed, dateFilter.startDate(), dateFilter.endDate());
        } else {
            notificationPage = repo.findAll(pageable, recipientId, eventId, type, viewed, sentAt);
        }
        return mapper.readPage(notificationPage);
    }
}
