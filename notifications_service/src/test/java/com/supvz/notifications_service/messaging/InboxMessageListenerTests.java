package com.supvz.notifications_service.messaging;

import com.fasterxml.jackson.databind.ObjectMapper;
import com.supvz.notifications_service.core.exception.InboxEventNotSerializedException;
import com.supvz.notifications_service.model.dto.InboxMessage;
import com.supvz.notifications_service.model.entity.InboxEventType;
import com.supvz.notifications_service.service.initializer.InboxInitializer;
import lombok.SneakyThrows;
import org.junit.jupiter.api.Assertions;
import org.junit.jupiter.api.BeforeEach;
import org.junit.jupiter.api.Test;
import org.junit.jupiter.api.extension.ExtendWith;
import org.mockito.Mock;
import org.mockito.junit.jupiter.MockitoExtension;
import org.springframework.amqp.core.Message;

import java.io.IOException;
import java.util.List;

import static org.mockito.Mockito.*;

@ExtendWith(MockitoExtension.class)
class InboxMessageListenerTests {
    InboxMessageListener target;
    @Mock
    ObjectMapper objectMapper;
    @Mock
    InboxInitializer initializer;
    @Mock
    InboxEventType eventType;
    @Mock


    Message messageMock;
    byte[] messageBodyMock;

    @BeforeEach
    void setUp() {
        messageBodyMock = new byte[0];
        messageMock = new Message(messageBodyMock);

        lenient().when(initializer.getType()).thenReturn(eventType);

        List<InboxInitializer> initializerList = List.of(initializer);

        target = new InboxMessageListener(objectMapper, initializerList);
    }

    @SneakyThrows
    @Test
    void listenSuccess() {
        InboxMessage inboxMessageMock = new InboxMessage(null, eventType, null);

        when(objectMapper.readValue(messageBodyMock, InboxMessage.class)).thenReturn(inboxMessageMock);
        doNothing().when(initializer).initialize(inboxMessageMock);

        Assertions.assertDoesNotThrow(() -> target.listen(messageMock));

        verify(objectMapper, times(1)).readValue(messageBodyMock, InboxMessage.class);
        verify(initializer, times(1)).initialize(inboxMessageMock);
    }

    @SneakyThrows
    @Test
    void listenFailed__UnhandledEventType() {
        InboxEventType unhandledEventType = mock(InboxEventType.class);
        InboxMessage inboxMessageMock = new InboxMessage(null, unhandledEventType, null);

        when(objectMapper.readValue(messageBodyMock, InboxMessage.class)).thenReturn(inboxMessageMock);

        Assertions.assertDoesNotThrow(() -> target.listen(messageMock));

        verify(objectMapper, times(1)).readValue(messageBodyMock, InboxMessage.class);
        verify(initializer, never()).initialize(any());
    }

    @SneakyThrows
    @Test
    void listenFailed__NotSerializedEvent() {
        when(objectMapper.readValue(messageBodyMock, InboxMessage.class)).thenThrow(IOException.class);

        Assertions.assertThrows(InboxEventNotSerializedException.class, () -> target.listen(messageMock));

        verify(objectMapper, times(1)).readValue(messageBodyMock, InboxMessage.class);
        verify(initializer, never()).initialize(any());
    }
}