package com.supvz.notifications_service.inbox;

import com.supvz.notifications_service.core.dto.InboxEventDto;
import com.supvz.notifications_service.core.dto.MessageDto;
import com.supvz.notifications_service.entity.InboxEvent;

public interface InboxEventMapper {
    InboxEvent create(MessageDto messageDto);

    InboxEventDto read(InboxEvent inboxEvent);
}
