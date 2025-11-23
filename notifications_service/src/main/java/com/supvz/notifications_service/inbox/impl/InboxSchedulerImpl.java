package com.supvz.notifications_service.inbox.impl;

import com.supvz.notifications_service.inbox.InboxEventService;
import com.supvz.notifications_service.inbox.InboxScheduler;
import com.supvz.notifications_service.service.EventProcessingService;
import lombok.RequiredArgsConstructor;
import lombok.extern.slf4j.Slf4j;
import org.springframework.beans.factory.annotation.Value;
import org.springframework.scheduling.annotation.Async;
import org.springframework.scheduling.annotation.Scheduled;
import org.springframework.stereotype.Service;

import java.util.List;
import java.util.UUID;

@Slf4j
@Service
@RequiredArgsConstructor
public class InboxSchedulerImpl implements InboxScheduler {
    private final InboxEventService inboxEventService;
    private final EventProcessingService processingService;

    @Value("${app.inbox.polling.batch-size}")
    private Integer batchSize;

    @Override
    @Scheduled(fixedDelayString = "${app.inbox.polling.delay-ms:10000}")
    @Async("inboxProcessingExecutor")
    public void pollForProcessing() {
        log.debug("Polling [PROCESS] inbox events.");
        List<UUID> reservedBatch = inboxEventService.readAndReserveUnprocessedBatch(batchSize);
        log.debug("Found and reserved batch of events. Size [{}]", reservedBatch.size());
        if (!reservedBatch.isEmpty()) {
            for (UUID eventId : reservedBatch) {
                processingService.processNotification(eventId);
            }
        }
    }

    @Override
    @Scheduled(fixedDelayString = "${app.inbox.polling.delay-ms:10000}")
    @Async("inboxCleaningExecutor")
    public void pollForCleaning() {
        log.debug("Polling [CLEAN] inbox events.");
        List<UUID> batch = inboxEventService.deleteFailedBatch(batchSize);
        log.debug("Failed inbox events are deleted, size: [{}].", batch.size());
    }
}