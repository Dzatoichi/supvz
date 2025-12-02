package com.supvz.notifications_service.mapper;

import com.supvz.notifications_service.model.dto.NotificationDto;
import org.springframework.mail.SimpleMailMessage;

public interface MailMapper {
    SimpleMailMessage message(NotificationDto notification);
}
