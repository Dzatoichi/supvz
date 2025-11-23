package com.supvz.notifications_service.service.impl;

import com.supvz.notifications_service.core.exception.NotificationProcessingException;
import com.supvz.notifications_service.model.entity.Notification;
import com.supvz.notifications_service.mapper.MailMapper;
import com.supvz.notifications_service.service.EmailNotificationProcessingService;
import lombok.RequiredArgsConstructor;
import lombok.extern.slf4j.Slf4j;
import org.springframework.mail.MailException;
import org.springframework.mail.SimpleMailMessage;
import org.springframework.mail.javamail.JavaMailSender;
import org.springframework.retry.annotation.Retryable;
import org.springframework.stereotype.Service;

/**
 * <h3>
 * Реализация сервиса для отправки электронных писем-уведомлений.
 * </h3>
 */
@Slf4j
@Service
@RequiredArgsConstructor
public class EmailNotificationProcessingServiceImpl implements EmailNotificationProcessingService {
    private final JavaMailSender mailSender;
    private final MailMapper mapper;

    @Override
    @Retryable(retryFor = MailException.class, maxAttemptsExpression = "${app.notification.number-retry-attempts}")
    public void send(Notification notification) {
        log.debug("Sending email notification [{}] to [{}].", notification.getId(), notification.getRecipientId());
        try {
            validate(notification);
            SimpleMailMessage mailMessage = mapper.mail(notification);
            mailSender.send(mailMessage);
            log.info("Email notification [{}] is sent.", notification.getId());
        } catch (MailException e) {
            log.error("Couldn't send email notification [{}].", notification.getId(), e);
            throw e;
        }
    }

    private void validate(Notification notification) {
        if (notification.getBody() == null || notification.getBody().isBlank())
            throw new NotificationProcessingException("Validation failed. Invalid body.");
        if (notification.getRecipientId() == null || notification.getRecipientId().isBlank())
            throw new NotificationProcessingException("Validation failed. Invalid recipient.");
        if (notification.getSubject() == null || notification.getSubject().isBlank())
            throw new NotificationProcessingException("Validation failed. Invalid subject.");
    }
}
