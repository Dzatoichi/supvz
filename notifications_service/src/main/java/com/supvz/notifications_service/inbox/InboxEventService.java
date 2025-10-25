package com.supvz.notifications_service.inbox;

import com.supvz.notifications_service.core.dto.MessageDto;
import com.supvz.notifications_service.entity.InboxEvent;

import java.util.List;
import java.util.UUID;

public interface InboxEventService {
    InboxEvent create(MessageDto messageDto);

    List<InboxEvent> readFirstUnprocessed(int firstNumber);

    void reserveEvent(InboxEvent event);
}
