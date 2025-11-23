package com.supvz.notifications_service.model.dto;


import com.supvz.notifications_service.model.entity.InboxEventType;
import com.supvz.notifications_service.model.entity.NotificationType;

import java.time.LocalDateTime;
import java.util.UUID;

public record InboxEventPayload(
        UUID eventId,
        InboxEventType eventType,
//    todo: изменить sql
        String payload,
//       todo:  это антипатерн. строка пейлоада
        LocalDateTime createdAt
//        todo: походу тут не должно быть такого поля
) {
}

// todo: пересмотреть текущий вид MessageDto. он не событийный
// Событие должно быть:
// Event → InboxEvent → Notification
