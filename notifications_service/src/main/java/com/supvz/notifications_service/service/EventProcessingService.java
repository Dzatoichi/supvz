package com.supvz.notifications_service.service;

import com.supvz.notifications_service.model.dto.MessageDto;

import java.util.UUID;

public interface EventProcessingService {
    void initNotification(MessageDto messageDto);

    void processNotification(UUID eventId);
}
