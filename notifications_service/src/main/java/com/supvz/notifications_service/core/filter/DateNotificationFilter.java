package com.supvz.notifications_service.core.filter;

import java.time.LocalDateTime;

public record DateNotificationFilter(
        LocalDateTime startDate,
        LocalDateTime endDate
) {
}
