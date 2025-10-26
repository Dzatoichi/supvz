package com.supvz.notifications_service.service.impl;

import com.supvz.notifications_service.entity.Notification;
import com.supvz.notifications_service.mapper.MailMapper;
import com.supvz.notifications_service.service.EmailNotificationProcessingService;
import lombok.RequiredArgsConstructor;
import lombok.extern.slf4j.Slf4j;
import org.springframework.mail.MailSender;
import org.springframework.mail.SimpleMailMessage;
import org.springframework.mail.javamail.JavaMailSender;
import org.springframework.stereotype.Service;

@Slf4j
@Service
@RequiredArgsConstructor
public class EmailNotificationProcessingServiceImpl implements EmailNotificationProcessingService {
    private final JavaMailSender mailSender;
    private final MailMapper mapper;

    @Override
    public void send(Notification notification) {
        log.debug("Sending email notification [{}].", notification.getId());
//        todo: validate notification for email
        SimpleMailMessage mailMessage = mapper.mail(notification);
        mailSender.send(mailMessage);

        log.info("Email notification [{}] is sent.", notification.getId());
    }
}
