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
    private final NotificationService notificationService;

    @Scheduled(fixedDelayString = "${app.notification.schedule.cleaning.delay-ms}")
    public void pollingForCleaningOldNotifications() {
        log.debug("По расписанию метод [CLEAN] старых нотификаций.");
        List<Integer> deletedBatch = notificationService.deleteOldNotifications();
        if (!deletedBatch.isEmpty())
            log.debug("Старые нотификации успешно удалены. Размер удаленного батча: [{}].", deletedBatch.size());
    }
}