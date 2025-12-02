package com.supvz.notifications_service.service.impl;

import com.supvz.notifications_service.model.dto.NotificationDto;
import com.supvz.notifications_service.mapper.MailMapper;
import com.supvz.notifications_service.model.entity.NotificationType;
import com.supvz.notifications_service.service.NotificationProcessor;
import lombok.RequiredArgsConstructor;
import lombok.extern.slf4j.Slf4j;
import org.springframework.mail.MailException;
import org.springframework.mail.SimpleMailMessage;
import org.springframework.mail.javamail.JavaMailSender;
import org.springframework.stereotype.Service;
import org.springframework.transaction.annotation.Propagation;
import org.springframework.transaction.annotation.Transactional;

/**
 * <h3>
 * Реализация процессора для обработки нотификаций типа email.
 * </h3>
 * Следует паттерну Strategy.
 */
@Slf4j
@Service
@RequiredArgsConstructor
public class EmailNotificationProcessor implements NotificationProcessor {
    private final JavaMailSender mailSender;
    private final MailMapper mapper;

    /**
     * Отправка нотификации типа email.
     * @param notification ДТО нотификации.
     */
    @Override
    @Transactional(propagation = Propagation.NOT_SUPPORTED)
    public void send(NotificationDto notification) {
        log.debug("Sending email notification [{}] to [{}].", notification.id(), notification.recipientId());
        try {
            SimpleMailMessage mailMessage = mapper.message(notification);
            mailSender.send(mailMessage);
            log.info("Email notification [{}] is sent.", notification.id());
        } catch (MailException ex) {
            log.error("Couldn't send email notification [{}].", notification.id(), ex);
            throw ex;
        }
    }

    /**
     * Метод для реализации паттерна Strategy.
     * @return NotificationType - тип нотификации, с которым работает процессор.
     */
    @Override
    public NotificationType getType() {
        return NotificationType.email;
    }
}