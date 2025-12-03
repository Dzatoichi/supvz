package com.supvz.notifications_service.service.sender;

import com.supvz.notifications_service.model.dto.NotificationDto;
import com.supvz.notifications_service.model.entity.NotificationType;
import lombok.extern.slf4j.Slf4j;
import org.springframework.stereotype.Service;
import org.springframework.transaction.annotation.Propagation;
import org.springframework.transaction.annotation.Transactional;

/**
 * <h3>
 * Реализация процессора для обработки нотификаций типа push.
 * </h3>
 * Следует паттерну Strategy.
 * <br/>
 * <br/>
 * Данный класс не реализован до момента создания десктопного-мобильного приложения.
 */
@Slf4j
@Service
public class PushNotificationSender implements NotificationSender {
    @Override
    @Transactional(propagation = Propagation.NOT_SUPPORTED)
    public void send(NotificationDto notification) {
        log.debug("Отправка 'push' нотификации [{}].", notification.id());
    }

    /**
     * Метод для реализации паттерна Strategy.
     *
     * @return NotificationType - тип нотификации, с которым работает процессор.
     */
    @Override
    public NotificationType getType() {
        return NotificationType.push;
    }
}
