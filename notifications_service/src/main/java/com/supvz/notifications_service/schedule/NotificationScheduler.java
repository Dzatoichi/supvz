package com.supvz.notifications_service.schedule;

import com.supvz.notifications_service.service.entity.NotificationService;
import lombok.RequiredArgsConstructor;
import lombok.extern.slf4j.Slf4j;
import org.springframework.scheduling.annotation.Scheduled;
import org.springframework.stereotype.Component;

import java.util.List;

@Slf4j
@Component
@RequiredArgsConstructor
public class NotificationScheduler {
    private final NotificationService service;

    @Scheduled(fixedDelayString = "${app.notification.schedule.cleaning.delay-ms}")
    public void cleanOldNotifications() {
        log.debug("SCHEDULE [CLEAN] old notifications.");
        List<Integer> deleted = service.deleteOldNotifications();
        if (!deleted.isEmpty())
            log.debug("Count of deleted old notifications: [{}].", deleted.size());
    }
}