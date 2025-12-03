package com.supvz.notifications_service.service.processor;

import com.supvz.notifications_service.core.exception.NotificationConflictException;
import com.supvz.notifications_service.core.exception.NotificationIsNotSentException;
import com.supvz.notifications_service.model.entity.InboxEventType;
import com.supvz.notifications_service.service.entity.InboxService;
import com.supvz.notifications_service.service.entity.NotificationService;
import lombok.RequiredArgsConstructor;
import lombok.extern.slf4j.Slf4j;
import org.springframework.stereotype.Service;

import java.util.UUID;

/**
 * <h3>
 * Реализация процессора для обработки inbox событий типа notification
 * </h3>
 * Следует паттерну Strategy.
 */
@Slf4j
@Service
@RequiredArgsConstructor
public class InboxNotificationProcessor implements InboxProcessor {
    private final InboxService inboxService;
    private final NotificationService notificationService;

    /**
     * Обработка inbox событий типа notification.
     *
     * @param eventId идентификатор события.
     */
    @Override
    public void process(UUID eventId) {
        log.debug("Обработка inbox 'notification' события [{}].", eventId);
        try {
            notificationService.processByEventId(eventId);
            inboxService.setProcessed(eventId);
            log.info("Inbox 'notification' событие [{}] успешно обработано.", eventId);
        } catch (NotificationConflictException ex) {
            log.warn("Конфликт с нотификацией по событию [{}]: {}", eventId, ex.getMessage());
            inboxService.setProcessed(eventId);
        } catch (NotificationIsNotSentException ex) {
            log.warn("Не получилось обработать нотификацию по событию [{}].", eventId, ex);
            inboxService.setCleanAfter(eventId);
        } catch (RuntimeException ex) {
            log.error("Неожиданное runtime исключение при обработке inbox 'notification' события [{}].", eventId, ex);
            inboxService.setCleanAfter(eventId);
        }
    }

    /**
     * Метод для реализации паттерна Strategy.
     *
     * @return InboxEventType - тип события, с которым работает процессор.
     */
    @Override
    public InboxEventType getType() {
        return InboxEventType.notification;
    }
}