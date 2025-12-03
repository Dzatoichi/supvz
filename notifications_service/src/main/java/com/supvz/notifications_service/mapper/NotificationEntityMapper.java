package com.supvz.notifications_service.mapper;

import com.fasterxml.jackson.databind.ObjectMapper;
import com.supvz.notifications_service.model.dto.NotificationDto;
import com.supvz.notifications_service.model.dto.PageDto;
import com.supvz.notifications_service.model.dto.NotificationPayload;
import com.supvz.notifications_service.model.entity.InboxEvent;
import com.supvz.notifications_service.model.entity.Notification;
import com.supvz.notifications_service.model.entity.NotificationType;
import lombok.RequiredArgsConstructor;
import lombok.extern.slf4j.Slf4j;
import org.springframework.data.domain.Page;
import org.springframework.stereotype.Component;

import java.time.LocalDateTime;
import java.util.List;

/**
 * <h3>
 * Маппер для работы с сущностью Notification.
 * </h3>
 */
@Slf4j
@Component
@RequiredArgsConstructor
public class NotificationEntityMapper implements NotificationMapper {
    private final ObjectMapper objectMapper;

    /**
     * Маппинг полезной нагрузки в сущность.
     * @param event сущность события, по которому создается нотификация.
     * @param payload полезная нагрузка.
     * @return Notification - сущность нотификации для последующего сохранения в БД.
     */
    @Override
    public Notification create(InboxEvent event, NotificationPayload payload) {
        NotificationType type = payload.type();
        Notification build = Notification.builder()
                .event(event)
                .notificationType(type)
                .body(payload.body())
                .subject(payload.subject())
                .recipientId(payload.recipientId())
                .build();
        if (type == NotificationType.push || type == NotificationType.web) {
            build.setViewed(false);
        }
        return build;
    }

    /**
     * Маппинг сущности нотификации в ДТО для передачи между слоями.
     * @param notification сущность нотификаиии.
     * @return NotificationDto - ДТО нотификации.
     */
    @Override
    public NotificationDto read(Notification notification) {
        return NotificationDto.builder()
                .id(notification.getId())
                .body(notification.getBody())
                .subject(notification.getSubject())
                .viewed(notification.getViewed())
                .sentAt(notification.getSentAt())
                .recipientId(notification.getRecipientId())
                .notificationType(notification.getNotificationType())
                .build();
    }

    /**
     * Маркировка нотификации как отправленной.
     * <br/>
     * <br/>
     * В случае, если сообщение уже отправлено, метод ничего не делает.
     * @param notification сущность нотификации.
     */
    @Override
    public void markAsSent(Notification notification) {
        if (notification.getSent())
            return;
        notification.setSentAt(LocalDateTime.now());
        notification.setSent(true);
    }

    /**
     *  Метод для маппинга страницы нотификаций в страницу ДТО.
     * @param page страница с сущностями.
     * @return PageDto - страница с сущностями ДТО
     */
    @Override
    public PageDto<NotificationDto> readPage(Page<Notification> page) {
        List<NotificationDto> content = page.getContent().stream().map(this::read).toList();
        return PageDto.<NotificationDto>builder()
                .content(content)
                .page(page.getNumber())
                .size(page.getSize())
                .total(page.getTotalPages())
                .hasNext(page.hasNext())
                .hasPrev(page.hasPrevious())
                .build();
    }
}
