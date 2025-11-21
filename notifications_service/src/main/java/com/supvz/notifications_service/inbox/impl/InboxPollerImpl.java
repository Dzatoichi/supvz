package com.supvz.notifications_service.inbox.impl;

import com.supvz.notifications_service.model.entity.InboxEvent;
import com.supvz.notifications_service.inbox.InboxEventService;
import com.supvz.notifications_service.inbox.InboxPoller;
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
public class InboxPollerImpl implements InboxPoller {
    private final InboxEventService inboxEventService;
    private final EventProcessingService processingService;

    @Value("${app.inbox.polling.to_process_by_time.number}")
    private int firstNumber;

    @Override
    @Scheduled(fixedDelay = 10000)
    public void poll() {
        log.debug("Polling inbox events.");
        List<InboxEvent> events = inboxEventService.readFirstUnprocessed(firstNumber);
        List<UUID> eventsIds = reserveEvents(events);
        for (UUID eventId : eventsIds) {
            processingService.processNotification(eventId);
        }
    }

    private List<UUID> reserveEvents(List<InboxEvent> events) {
        List<UUID> eventsIds = events.stream().map(InboxEvent::getEventId).toList();
        log.debug("Reserve events {}.", eventsIds.isEmpty() ? "[EMPTY LIST]" : eventsIds);

        for (InboxEvent event : events) {
            inboxEventService.reserveEvent(event);
        }
        return eventsIds;
    }
}
