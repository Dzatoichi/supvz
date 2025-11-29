package com.supvz.notifications_service.model.dto;

import com.supvz.notifications_service.model.entity.NotificationType;
import jakarta.validation.constraints.NotBlank;
import jakarta.validation.constraints.NotNull;

public record NotificationPayload(
        @NotNull
        NotificationType type,
        @NotBlank
        String recipientId,
        @NotBlank
        String body,
        @NotBlank
        String subject) implements InboxEventPayload {
}
