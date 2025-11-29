package com.supvz.notifications_service.inbox.impl;

import com.supvz.notifications_service.inbox.InboxEventService;
import com.supvz.notifications_service.inbox.InboxScheduler;
import com.supvz.notifications_service.service.EventProcessingService;
import lombok.RequiredArgsConstructor;
import lombok.extern.slf4j.Slf4j;
import org.springframework.beans.factory.annotation.Value;
import org.springframework.scheduling.annotation.Scheduled;
import org.springframework.stereotype.Service;

import java.util.List;
import java.util.UUID;
import java.util.concurrent.Executor;

@Slf4j
@Service
@RequiredArgsConstructor
public class InboxSchedulerImpl implements InboxScheduler {
    private final InboxEventService inboxEventService;
    private final EventProcessingService processingService;
    private final Executor notificationProcessingExecutor;
    @Value("${app.inbox.polling.processing.batch-size}")
    private Integer processingBatchSize;
    @Value("${app.inbox.polling.cleaning.batch-size}")
    private Integer cleaningBatchSize;

    @Override
    @Scheduled(fixedDelayString = "${app.inbox.polling.processing.delay-ms:10000}")
    public void pollForProcessing() {
        log.debug("Polling [PROCESS] inbox events.");
        List<UUID> reservedBatch = inboxEventService.readAndReserveUnprocessedBatch(processingBatchSize);
        log.debug("Found and reserved batch of events. Size [{}]", reservedBatch.size());
        if (!reservedBatch.isEmpty()) {
            for (UUID eventId : reservedBatch) {
                notificationProcessingExecutor.execute(() ->
                        processingService.processNotification(eventId));
            }
        }
//        todo: не вычитывать из бд и ниче не делать, если пул потоков уже занят.
    }

    @Override
    @Scheduled(fixedDelayString = "${app.inbox.polling.cleaning.delay-ms:5000}")
    public void pollForCleaning() {
        log.debug("Polling [CLEAN] inbox events.");
        List<UUID> batch = inboxEventService.deleteFailedBatch(cleaningBatchSize);
        log.debug("Failed inbox events are deleted, size: [{}].", batch.size());
    }
//    todo: удалять те, которые просмотрены и прошла неделя или нечекнутые + месяц.
//     То есть создать новый щедулед метод.
}