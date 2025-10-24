package com.supvz.notifications_service.service;

import com.supvz.notifications_service.core.dto.MessageDto;

import java.util.UUID;

public interface MessageProcessingService {
    void initNotification(MessageDto messageDto);

    void processNotification(UUID eventId);
}
