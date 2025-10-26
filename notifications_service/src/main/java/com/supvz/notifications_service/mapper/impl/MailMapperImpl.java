package com.supvz.notifications_service.mapper.impl;

import com.supvz.notifications_service.entity.Notification;
import com.supvz.notifications_service.mapper.MailMapper;
import org.springframework.beans.factory.annotation.Value;
import org.springframework.mail.SimpleMailMessage;
import org.springframework.stereotype.Component;

@Component
public class MailMapperImpl implements MailMapper {
    @Value("${spring.mail.username}")
    private String from;

    @Override
    public SimpleMailMessage mail(Notification notification) {
        SimpleMailMessage mailMessage = new SimpleMailMessage();
        mailMessage.setFrom(from);
        mailMessage.setSubject(notification.getSubject());
        mailMessage.setTo(notification.getRecipientId());
        mailMessage.setText(notification.getBody());
//        todo: есть возможность отправлять нескольким почтам сразу (mailMessage.setTo(... String to))

        return mailMessage;
    }
}
