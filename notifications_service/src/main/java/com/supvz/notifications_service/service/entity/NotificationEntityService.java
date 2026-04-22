package com.supvz.notifications_service.service.entity;

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
import com.supvz.notifications_service.service.sender.NotificationSender;
import com.supvz.notifications_service.util.NotificationSpecifications;
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

/**
 * <h3>
 * Реализация сервиса для обработки сущностей Notification.
 * </h3>
 */
@Slf4j
@Service
public class NotificationEntityService implements NotificationService {
    private final NotificationMapper mapper;
    private final NotificationRepository repo;
    private final Map<NotificationType, NotificationSender> senders;
    @Value("${app.notification.schedule.cleaning.ttl.email-days}")
    private Integer emailTtlDays;
    @Value("${app.notification.schedule.cleaning.ttl.viewed-days}")
    private Integer viewedTtlDays;
    @Value("${app.notification.schedule.cleaning.ttl.not-viewed-days}")
    private Integer notViewedTtlDays;

    /**
     * Конструктор.
     */
    @Autowired
    public NotificationEntityService(
            NotificationMapper mapper,
            NotificationRepository repo,
            List<NotificationSender> senderList
    ) {
        this.mapper = mapper;
        this.repo = repo;
        this.senders = senderList.stream()
                .collect(Collectors.toMap(NotificationSender::getType, Function.identity()));
    }

    /**
     * Создание сущности нотификации на основе inbox события.
     *
     * @param event               событие, на основе которого создается нотификация.
     * @param notificationPayload полезная нагрузка нотификации из события.
     */
    @Override
    @Transactional
    public void create(InboxEvent event, NotificationPayload notificationPayload) {
        log.debug("Создание сущности нотификации [{}] по событию [{}].", event.getEventType(), event.getEventId());
        Notification mapped = mapper.create(event, notificationPayload);
        Notification saved = repo.save(mapped);
        log.info("Сущность нотификации [{}] по событию [{}] успешно создано.", saved.getId(), event.getEventId());
    }

    /**
     * Получение страницы нотификаций с фильтрацией.
     *
     * @param page   номер страницы.
     * @param size   кол-во нотификаций на странице.
     * @param filter класс, содержащий параметры фильтрации.
     * @return PageDto - страница с ДТО нотификациями.
     */
    @Override
    public PageDto<NotificationDto> findAll(int page, int size, NotificationFilter filter) {
        log.debug("Получение страницы. Номер: [{}], размер: [{}].", page, size);
        Pageable pageable = PageRequest.of(page, size);
        Specification<Notification> spec = configureSpecification(filter);
        Page<Notification> notificationPage = repo.findAll(spec, pageable);
        return mapper.readPage(notificationPage);
    }

    /**
     * Настройка спецификаций для создания динамического запроса с фильтрацией.
     *
     * @param filter параметры фильтрации.
     * @return Specification - спецификация, настройка запроса.
     */
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

    /**
     * Обработка нотификации по событию.
     *
     * @param eventId идентификатор события.
     */
    @Override
    @Transactional
    public void processByEventId(UUID eventId) {
        Notification notification = repo.findByEventId(eventId)
                .orElseThrow(() -> new NotificationNotFoundException("Нотификация по событию [%s] не найдена."
                        .formatted(eventId)));
        NotificationDto dto = mapper.read(notification);
        log.debug("Обработка нотификации [{}].", notification.getId());
        if (notification.getSent()) throw new NotificationConflictException(
                "Нотификация [%s] уже отправлена.".formatted(notification.getId()));
        try {
            senders.get(dto.notificationType()).send(dto);
        } catch (RuntimeException ex) {
            log.warn("Исключение в процессе обработки нотификации [{}].", notification.getId());
            throw new NotificationIsNotSentException(ex.getMessage());
        }
        mapper.markAsSent(notification);
        repo.save(notification);
        log.debug("Нотификация [{}] успешно обработана.", notification.getId());
    }

    /**
     * Удаление старых нотификаций по настроенным параметрам TTL.
     *
     * @return List - список удаленных нотификаций.
     */
    @Override
    public List<Integer> deleteOldNotifications() {
        return repo.deleteOldNotifications(viewedTtlDays, notViewedTtlDays, emailTtlDays);
    }

    @Override
    public void setViewed(Long notificationId) {
        Notification notification = repo.findById(notificationId)
                .orElseThrow(() -> new NotificationNotFoundException("Нотификация [%s] не была найдена."
                        .formatted(notificationId)));
        notification.setViewed(true);
        repo.save(notification);
        log.info("Нотификация [{}] была просмотрена.", notificationId);
    }
}