package com.supvz.notifications_service.mapper;

import com.supvz.notifications_service.model.dto.NotificationDto;
import org.springframework.beans.factory.annotation.Value;
import org.springframework.mail.SimpleMailMessage;
import org.springframework.stereotype.Component;

/**
 * <h3>
 * Маппер для создания нотификаций типа email.
 * </h3>
 */
@Component
public class SimpleMailMapper implements MailMapper {
    @Value("${spring.mail.username}")
    private String from;

    /**
     *  Маппинг нотификации в электронное письмо.
     * @param notification ДТО нотификации.
     * @return SimpleMailMessage - представление эл. письма.
     */
    @Override
    public SimpleMailMessage message(NotificationDto notification) {
        SimpleMailMessage mailMessage = new SimpleMailMessage();
        mailMessage.setFrom(from);
        mailMessage.setSubject(notification.subject());
        mailMessage.setTo(notification.recipientId());
        mailMessage.setText(notification.body());
        return mailMessage;
    }
}