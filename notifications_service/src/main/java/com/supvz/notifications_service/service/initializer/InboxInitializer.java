package com.supvz.notifications_service.service.initializer;

import com.fasterxml.jackson.core.JsonProcessingException;
import com.supvz.notifications_service.model.dto.InboxMessage;
import com.supvz.notifications_service.model.entity.InboxEventType;

public interface InboxInitializer {
    void initialize(InboxMessage payload) throws JsonProcessingException;

    InboxEventType getType();
}
