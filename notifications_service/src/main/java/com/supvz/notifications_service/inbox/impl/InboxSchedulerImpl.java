package com.supvz.notifications_service.inbox.impl;

import com.supvz.notifications_service.model.entity.InboxEvent;
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
    public void poll() {
        log.debug("Polling inbox events.");
        List<UUID> reservedBatch = inboxEventService.readAndReserveUnprocessedBatch(batchSize);
        log.debug("Found and reserved batch of events. Size [{}]", reservedBatch.size());
        if (!reservedBatch.isEmpty()) {
            for (UUID eventId : reservedBatch) {
//            todo: сделать try-catch. Если один ивент упадет -- весь полер остановится
                try {
                    processingService.processNotification(eventId);
//                    todo: может, можно это сделать асинхронно? либо на каждую нотификацию поток(это мне больше нравится)
                } catch (RuntimeException e) {
                    log.error("Couldn't process notification by event [{}]", eventId, e);
                }
            }
        }
    }
}
