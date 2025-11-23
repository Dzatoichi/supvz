package com.supvz.notifications_service.service.impl;

import com.supvz.notifications_service.model.entity.Notification;
import com.supvz.notifications_service.mapper.MailMapper;
import com.supvz.notifications_service.service.EmailNotificationProcessingService;
import lombok.RequiredArgsConstructor;
import lombok.extern.slf4j.Slf4j;
import org.springframework.mail.MailException;
import org.springframework.mail.SimpleMailMessage;
import org.springframework.mail.javamail.JavaMailSender;
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
    public void send(Notification notification) {
        log.debug("Sending email notification [{}].", notification.getId());
        try {
//            todo: валидация данных до отправки
            SimpleMailMessage mailMessage = mapper.mail(notification);
            mailSender.send(mailMessage);
//            todo: как оказывается, smtp не гарантирует успешную доставку писем. Придумать компенсирующее событие.
            log.info("Email notification [{}] is sent.", notification.getId());
        } catch (MailException e) {
            log.error("Couldn't send email notification [{}]: {}.", notification.getId(), e.getMessage());
//            todo: логировать сам объект ошибки является нехорошей практикой.
            throw e;
        }
    }
}
