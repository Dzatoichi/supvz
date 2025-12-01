package com.supvz.notifications_service.model.dto;

import com.fasterxml.jackson.annotation.JsonSubTypes;
import com.fasterxml.jackson.annotation.JsonTypeInfo;

@JsonTypeInfo(
        use = JsonTypeInfo.Id.NAME,
        include = JsonTypeInfo.As.EXTERNAL_PROPERTY,
        property = "eventType",
        visible = true
)
@JsonSubTypes({
        @JsonSubTypes.Type(value = NotificationPayload.class, name = "notification"),
        @JsonSubTypes.Type(value = OtherPayload.class, name = "other")
})
public interface InboxEventPayload {
}