package com.supvz.notifications_service.service.initializer;

import com.fasterxml.jackson.core.JsonProcessingException;
import com.fasterxml.jackson.databind.ObjectMapper;
import com.supvz.notifications_service.model.dto.InboxMessage;
import com.supvz.notifications_service.model.dto.NotificationPayload;
import com.supvz.notifications_service.model.entity.InboxEvent;
import com.supvz.notifications_service.model.entity.InboxEventType;
import com.supvz.notifications_service.service.entity.InboxService;
import com.supvz.notifications_service.service.entity.NotificationService;
import lombok.SneakyThrows;
import org.junit.jupiter.api.Test;
import org.junit.jupiter.api.extension.ExtendWith;
import org.mockito.InjectMocks;
import org.mockito.Mock;
import org.mockito.junit.jupiter.MockitoExtension;

import static org.junit.jupiter.api.Assertions.*;
import static org.mockito.Mockito.*;

@ExtendWith(MockitoExtension.class)
class NotificationInboxInitializerTests {
    @InjectMocks
    NotificationInboxInitializer target;
    @Mock
    InboxService inboxService;
    @Mock
    NotificationService notificationService;
    @Mock
    ObjectMapper objectMapper;
    @Mock
    NotificationPayload payloadMock;
    @Mock
    InboxEvent eventMock;


    @Test
    @SneakyThrows
    void initializeSuccess() {
        InboxMessage messageMock = new InboxMessage(null, InboxEventType.notification, "dummy");

        when(objectMapper.readValue("dummy", NotificationPayload.class)).thenReturn(payloadMock);
        when(inboxService.create(messageMock)).thenReturn(eventMock);
        doNothing().when(notificationService).create(eventMock, payloadMock);

        assertDoesNotThrow(() -> target.initialize(messageMock));

        verify(objectMapper, times(1)).readValue("dummy", NotificationPayload.class);
        verify(inboxService, times(1)).create(messageMock);
        verify(notificationService, times(1)).create(eventMock, payloadMock);
    }

    @Test
    @SneakyThrows
    void initializeFailed__NotSerialized() {
        InboxMessage messageMock = new InboxMessage(null, InboxEventType.notification, "dummy");

        when(objectMapper.readValue("dummy", NotificationPayload.class)).thenThrow(JsonProcessingException.class);

        assertThrows(JsonProcessingException.class, () -> target.initialize(messageMock));

        verify(objectMapper, times(1)).readValue("dummy", NotificationPayload.class);
        verify(inboxService, never()).create(messageMock);
        verify(notificationService, never()).create(eventMock, payloadMock);
    }

    @Test
    void testGetType() {
        assertEquals(InboxEventType.notification, target.getType());
    }
}