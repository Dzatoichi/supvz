package com.supvz.notifications_service.service.processor;

import com.supvz.notifications_service.core.exception.NotificationConflictException;
import com.supvz.notifications_service.core.exception.NotificationIsNotSentException;
import com.supvz.notifications_service.model.entity.InboxEventType;
import com.supvz.notifications_service.service.entity.InboxService;
import com.supvz.notifications_service.service.entity.NotificationService;
import org.junit.jupiter.api.Test;
import org.junit.jupiter.api.extension.ExtendWith;
import org.mockito.InjectMocks;
import org.mockito.Mock;
import org.mockito.junit.jupiter.MockitoExtension;

import java.util.UUID;

import static org.junit.jupiter.api.Assertions.*;
import static org.mockito.Mockito.*;

@ExtendWith(MockitoExtension.class)
class InboxNotificationProcessorTests {
    @InjectMocks
    InboxNotificationProcessor target;
    @Mock
    InboxService inboxService;
    @Mock
    NotificationService notificationService;

    @Test
    void processSuccess() {
        UUID eventIdMock = UUID.randomUUID();

        doNothing().when(notificationService).processByEventId(eventIdMock);
        doNothing().when(inboxService).setProcessed(eventIdMock);

        assertDoesNotThrow(() -> target.process(eventIdMock));

        verify(notificationService, times(1)).processByEventId(eventIdMock);
        verify(inboxService, times(1)).setProcessed(eventIdMock);
    }

    @Test
    void processConflict__NotificationAlreadyProcessed() {
        UUID eventIdMock = UUID.randomUUID();

        doThrow(NotificationConflictException.class).when(notificationService).processByEventId(eventIdMock);
        doNothing().when(inboxService).setProcessed(eventIdMock);

        assertDoesNotThrow(() -> target.process(eventIdMock));

        verify(notificationService, times(1)).processByEventId(eventIdMock);
        verify(inboxService, times(1)).setProcessed(eventIdMock);
    }

    @Test
    void processFailed__NotificationIsNotSent() {
        UUID eventIdMock = UUID.randomUUID();

        doThrow(NotificationIsNotSentException.class).when(notificationService).processByEventId(eventIdMock);
        doNothing().when(inboxService).setCleanAfter(eventIdMock);

        assertDoesNotThrow(() -> target.process(eventIdMock));

        verify(notificationService, times(1)).processByEventId(eventIdMock);
        verify(inboxService, never()).setProcessed(any());
        verify(inboxService, times(1)).setCleanAfter(eventIdMock);
    }

    @Test
    void processFailed__UnexpectedRuntimeException() {
        UUID eventIdMock = UUID.randomUUID();

        doThrow(RuntimeException.class).when(notificationService).processByEventId(eventIdMock);
        doNothing().when(inboxService).setCleanAfter(eventIdMock);

        assertDoesNotThrow(() -> target.process(eventIdMock));

        verify(notificationService, times(1)).processByEventId(eventIdMock);
        verify(inboxService, never()).setProcessed(any());
        verify(inboxService, times(1)).setCleanAfter(eventIdMock);
    }

    @Test
    void getTypeShouldReturnNotificationType() {
        assertEquals(InboxEventType.notification, target.getType());
    }

}