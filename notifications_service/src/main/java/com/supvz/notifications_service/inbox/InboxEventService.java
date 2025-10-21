package com.supvz.notifications_service.inbox;

import com.supvz.notifications_service.core.MessageDto;
import com.supvz.notifications_service.entity.InboxEvent;

public interface InboxEventService {
    InboxEvent create(MessageDto messageDto);
}
