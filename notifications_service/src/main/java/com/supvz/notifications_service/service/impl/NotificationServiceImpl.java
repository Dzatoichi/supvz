package com.supvz.notifications_service.service.impl;

import com.supvz.notifications_service.core.exception.*;
import com.supvz.notifications_service.model.dto.NotificationDto;
import com.supvz.notifications_service.model.dto.NotificationPayload;
import com.supvz.notifications_service.model.dto.PageDto;
import com.supvz.notifications_service.core.filter.DateNotificationFilter;
import com.supvz.notifications_service.core.filter.NotificationFilter;
import com.supvz.notifications_service.model.entity.InboxEvent;
import com.supvz.notifications_service.model.entity.Notification;
import com.supvz.notifications_service.model.entity.NotificationType;
import com.supvz.notifications_service.mapper.NotificationMapper;
import com.supvz.notifications_service.repo.NotificationRepository;
import com.supvz.notifications_service.service.EmailNotificationProcessingService;
import com.supvz.notifications_service.service.NotificationService;
import com.supvz.notifications_service.service.PushNotificationProcessingService;
import com.supvz.notifications_service.service.WebNotificationProcessingService;
import lombok.RequiredArgsConstructor;
import lombok.extern.slf4j.Slf4j;
import org.springframework.data.domain.Page;
import org.springframework.data.domain.PageRequest;
import org.springframework.data.domain.Pageable;
import org.springframework.stereotype.Service;
import org.springframework.transaction.annotation.Transactional;

import java.util.UUID;

@Slf4j
@Service
@RequiredArgsConstructor
public class NotificationServiceImpl implements NotificationService {
    private final NotificationMapper mapper;
    private final NotificationRepository repo;
    private final EmailNotificationProcessingService emailNotificationService;
    private final WebNotificationProcessingService webNotificationService;
    private final PushNotificationProcessingService pushNotificationService;

    @Override
    @Transactional
    public void create(InboxEvent event, NotificationPayload notificationPayload) {
        log.debug("Create notification by type [{}], by event [{}].", event.getEventType(), event.getEventId());
        Notification mapped = mapper.create(event, notificationPayload);
        Notification saved = repo.save(mapped);
        log.info("Notification [{}] by event [{}] is created.", saved.getId(), event.getEventId());
    }

    @Override
    public PageDto<NotificationDto> findAll(int page, int size, NotificationFilter filter) {
        log.debug("Read all. Page {}, size {}.", page, size);
        Pageable pageable = PageRequest.of(page, size);
        String recipientId = filter.recipientId();
        UUID eventId = filter.eventId();
        NotificationType type = filter.type();
        Boolean viewed = filter.viewed();
        DateNotificationFilter dateFilter = filter.dateFilter();
        boolean filterByDate = dateFilter != null && (dateFilter.startDate() != null && dateFilter.endDate() != null);
        Page<Notification> notificationPage;
        if (filterByDate) {
            notificationPage = repo.findAllWithDateFilter(pageable, recipientId,
                    eventId, type, viewed, dateFilter.startDate(), dateFilter.endDate());
        } else {
            notificationPage = repo.findAll(pageable, recipientId, eventId, type, viewed);
        }
        return mapper.readPage(notificationPage);
    }

    @Override
    @Transactional
    public void processByEventId(UUID eventId) {
        Notification notification = repo.findByEventId(eventId)
                .orElseThrow(() -> new NotificationNotFoundException("Notification by event [%s] was not found."
                        .formatted(eventId)));
        NotificationDto dto = mapper.read(notification);
        log.debug("Processing notification [{}].", notification.getId());
        if (notification.getSent()) throw new NotificationConflictException(
                "Notification [%s] already sent.".formatted(notification.getId()));
        try {
            sendNotification(dto);
        } catch (RuntimeException ex) {
            log.warn("Exception sending notification [{}].", notification.getId());
            throw new NotificationIsNotSentException(ex.getMessage());
        }
        mapper.markAsSent(notification);
        repo.save(notification);
        log.debug("Notification [{}] is sent.", notification.getId());
    }

    private void sendNotification(NotificationDto notificationDto) {
        switch (notificationDto.notificationType()) {
            case email -> emailNotificationService.send(notificationDto);
            case web -> webNotificationService.send(notificationDto);
            case push -> pushNotificationService.send(notificationDto);
        }

    }
}
