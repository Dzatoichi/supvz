package com.supvz.notifications_service.mapper;

import com.supvz.notifications_service.entity.Notification;
import org.springframework.mail.SimpleMailMessage;

public interface MailMapper {
    SimpleMailMessage mail(Notification notification);
}
