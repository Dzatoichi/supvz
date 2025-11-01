package com.supvz.notifications_service.inbox;

import com.supvz.notifications_service.model.dto.MessageDto;
import com.supvz.notifications_service.model.entity.InboxEvent;

import java.time.LocalDateTime;
import java.util.List;

public interface InboxEventService {
    InboxEvent create(MessageDto messageDto);

    List<InboxEvent> readFirstUnprocessed(int firstNumber);

    void reserveEvent(InboxEvent event);

    void markProcessed(InboxEvent event, LocalDateTime sentAndProcessedAt);
}
