package com.supvz.notifications_service.inbox.impl;

import com.supvz.notifications_service.core.dto.InboxEventDto;
import com.supvz.notifications_service.inbox.InboxEventService;
import com.supvz.notifications_service.inbox.InboxPoller;
import com.supvz.notifications_service.service.NotificationService;
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
    private final NotificationService notificationService;

    @Value("${inbox.polling.to_process_by_time.number}")
    private int firstNumber;

    @Override
    @Scheduled(fixedDelay = 10000)
    public void poll() {
        log.info("Polling inbox events.");
        List<UUID> eventIds = inboxEventService.readFirstUnprocessed(firstNumber);

        for (UUID eventId : eventIds) {
            notificationService.process(eventId);
        }
    }
}
