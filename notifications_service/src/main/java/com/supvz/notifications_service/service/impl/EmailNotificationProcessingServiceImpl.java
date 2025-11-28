package com.supvz.notifications_service.service.impl;

import com.supvz.notifications_service.core.exception.NotificationValidationException;
import com.supvz.notifications_service.model.dto.NotificationDto;
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
    public void send(NotificationDto notification) {
        log.debug("Sending email notification [{}] to [{}].", notification.id(), notification.recipientId());
        try {
//            validate(notification);
            SimpleMailMessage mailMessage = mapper.mail(notification);
            mailSender.send(mailMessage);
            log.info("Email notification [{}] is sent.", notification.id());
        } catch (MailException ex) {
            log.error("Couldn't send email notification [{}].", notification.id(), ex);
            throw ex;
        }
    }

//    private void validate(NotificationDto notification) {
//        if (notification.getBody() == null || notification.getBody().isBlank())
//            throw new NotificationValidationException("Validation failed. Invalid body.");
//        if (notification.getRecipientId() == null || notification.getRecipientId().isBlank())
//            throw new NotificationValidationException("Validation failed. Invalid recipient.");
//        if (notification.getSubject() == null || notification.getSubject().isBlank())
//            throw new NotificationValidationException("Validation failed. Invalid subject.");
//    }
//    todo: насколько целесообразно делать валидацию здесь, а не при получении ивента сразу?
//     разве не производительней будет получить и сразу его удалить, а не сохранять, доставать, пробовать обрабатывать?
//     как будто я сам уже ответил на вопрос :)
}
