package com.supvz.notifications_service.service.impl;

import com.supvz.notifications_service.core.exception.NotificationConflictException;
import com.supvz.notifications_service.core.exception.NotificationIsNotSentException;
import com.supvz.notifications_service.core.exception.NotificationNotFoundException;
import com.supvz.notifications_service.model.dto.NotificationDto;
import com.supvz.notifications_service.model.dto.NotificationPayload;
import com.supvz.notifications_service.model.dto.PageDto;
import com.supvz.notifications_service.core.filter.NotificationFilter;
import com.supvz.notifications_service.model.entity.InboxEvent;
import com.supvz.notifications_service.model.entity.Notification;
import com.supvz.notifications_service.mapper.NotificationMapper;
import com.supvz.notifications_service.model.entity.NotificationType;
import com.supvz.notifications_service.repo.NotificationRepository;
import com.supvz.notifications_service.util.NotificationSpecifications;
import com.supvz.notifications_service.service.*;
import lombok.extern.slf4j.Slf4j;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.beans.factory.annotation.Value;
import org.springframework.data.domain.Page;
import org.springframework.data.domain.PageRequest;
import org.springframework.data.domain.Pageable;
import org.springframework.data.jpa.domain.Specification;
import org.springframework.stereotype.Service;
import org.springframework.transaction.annotation.Transactional;

import java.util.List;
import java.util.Map;
import java.util.UUID;
import java.util.function.Function;
import java.util.stream.Collectors;

@Slf4j
@Service
public class NotificationEntityService implements NotificationService {
    private final NotificationMapper mapper;
    private final NotificationRepository repo;
    private final Map<NotificationType, NotificationProcessor> processors;
    @Value("${app.notification.schedule.cleaning.ttl.email-days}")
    private Integer emailTtlDays;
    @Value("${app.notification.schedule.cleaning.ttl.viewed-days}")
    private Integer viewedTtlDays;
    @Value("${app.notification.schedule.cleaning.ttl.not-viewed-days}")
    private Integer notViewedTtlDays;


    @Autowired
    public NotificationEntityService(NotificationMapper mapper, NotificationRepository repo, List<NotificationProcessor> processorList) {
        this.mapper = mapper;
        this.repo = repo;
        this.processors = processorList.stream()
                .collect(Collectors.toMap(NotificationProcessor::getType, Function.identity()));
    }

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
        Specification<Notification> spec = configureSpecification(filter);
        Page<Notification> notificationPage = repo.findAll(spec, pageable);
        return mapper.readPage(notificationPage);
    }

    private Specification<Notification> configureSpecification(NotificationFilter filter) {
        Specification<Notification> spec = NotificationSpecifications.hasRecipientId(filter.recipientId());
        spec = spec
                .and(NotificationSpecifications.hasEventId(filter.eventId()))
                .and(NotificationSpecifications.hasType(filter.type()))
                .and(NotificationSpecifications.isViewed(filter.viewed()))
                .and(NotificationSpecifications.isSent(filter.sent()))
                .and(NotificationSpecifications.likeSubject(filter.subject()))
                .and(NotificationSpecifications.likeBody(filter.body()))
                .and(NotificationSpecifications.betweenDates(filter.startDate(), filter.endDate()));
        return spec;
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
            processors.get(dto.notificationType()).send(dto);
        } catch (RuntimeException ex) {
            log.warn("Exception sending notification [{}].", notification.getId());
            throw new NotificationIsNotSentException(ex.getMessage());
        }
        mapper.markAsSent(notification);
        repo.save(notification);
        log.debug("Notification [{}] is sent.", notification.getId());
    }

    @Override
    public List<Integer> deleteOldNotifications() {
        return repo.deleteOldNotifications(viewedTtlDays, notViewedTtlDays, emailTtlDays);
    }
}