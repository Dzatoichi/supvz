package com.supvz.notifications_service.schedule;

import com.supvz.notifications_service.service.InboxProcessor;
import com.supvz.notifications_service.service.InboxService;
import com.supvz.notifications_service.model.entity.EventIdTypeProjection;
import com.supvz.notifications_service.model.entity.InboxEventType;
import lombok.extern.slf4j.Slf4j;
import org.springframework.beans.factory.annotation.Value;
import org.springframework.scheduling.annotation.Scheduled;
import org.springframework.stereotype.Component;

import java.util.List;
import java.util.Map;
import java.util.UUID;
import java.util.concurrent.Executor;
import java.util.function.Function;
import java.util.stream.Collectors;

@Slf4j
@Component
public class InboxScheduler {
    private final InboxService inboxService;
    private final Executor eventExecutor;
    private final Map<InboxEventType, InboxProcessor> processors;
    @Value("${app.inbox.schedule.processing.batch-size}")
    private Integer processingBatchSize;
    @Value("${app.inbox.schedule.cleaning.batch-size}")
    private Integer cleaningBatchSize;

    public InboxScheduler(
            InboxService inboxService,
            Executor eventExecutor,
            List<InboxProcessor> processorList
    ) {
        this.inboxService = inboxService;
        this.eventExecutor = eventExecutor;
        this.processors = processorList.stream()
                .collect(Collectors.toMap(InboxProcessor::getType, Function.identity()));
    }

    @Scheduled(fixedDelayString = "${app.inbox.schedule.processing.delay-ms}")
    public void pollForProcessing() {
        log.debug("SCHEDULE [PROCESS] inbox events.");
        List<EventIdTypeProjection> reservedBatch = inboxService.readAndReserveUnprocessedBatch(processingBatchSize);
        if (!reservedBatch.isEmpty())
            log.debug("Found and reserved batch of events. Size [{}]", reservedBatch.size());
        if (!reservedBatch.isEmpty()) {
            for (EventIdTypeProjection event : reservedBatch) {
                eventExecutor.execute(() ->
                        processors.get(event.getEventType()).process(event.getEventId()));
            }
        }
    }

    @Scheduled(fixedDelayString = "${app.inbox.schedule.cleaning.delay-ms}")
    public void pollForCleaning() {
        log.debug("SCHEDULE [CLEAN] inbox events.");
        List<UUID> batch = inboxService.deleteFailedBatch(cleaningBatchSize);
        if (!batch.isEmpty())
            log.debug("Failed inbox events are deleted, size: [{}].", batch.size());
    }
}