package com.supvz.notifications_service.inbox;

import com.supvz.notifications_service.model.dto.InboxEventDto;
import com.supvz.notifications_service.model.dto.MessageDto;
import com.supvz.notifications_service.model.entity.InboxEvent;

public interface InboxEventMapper {
    InboxEvent create(MessageDto messageDto);

    InboxEventDto read(InboxEvent inboxEvent);
}
