package com.supvz.notifications_service.mapper;

import com.supvz.notifications_service.model.dto.InboxMessage;
import com.supvz.notifications_service.model.entity.InboxEvent;
import com.supvz.notifications_service.model.entity.InboxEventType;
import org.junit.jupiter.api.Test;

import java.time.LocalDateTime;
import java.util.UUID;

import static org.junit.jupiter.api.Assertions.*;
import static org.mockito.Mockito.*;

class InboxEntityMapperTests {
    InboxEntityMapper target = new InboxEntityMapper();

    @Test
    void create() {
        UUID eventIdMock = UUID.randomUUID();
        InboxEventType eventTypeMock = mock(InboxEventType.class);
        String payloadMock = "payloadMock";
        InboxMessage messageMock = new InboxMessage(eventIdMock, eventTypeMock, payloadMock);
        InboxEvent expected = InboxEvent.builder()
                .eventType(eventTypeMock)
                .eventId(eventIdMock)
                .payload(payloadMock)
                .build();

        InboxEvent result = assertDoesNotThrow(() -> target.create(messageMock));
        assertEquals(expected, result);
    }

    @Test
    void markAsProcessed() {
        LocalDateTime timeMock = LocalDateTime.now().minusMinutes(10);
        InboxEvent eventMock = InboxEvent.builder()
                .processed(false)
                .processedAt(timeMock)
                .reservedTo(timeMock)
                .cleanAfter(timeMock)
                .build();

        assertDoesNotThrow(() -> target.markAsProcessed(eventMock));
        assertNotNull(eventMock.getProcessedAt());
        assertNotEquals(eventMock.getProcessedAt(), timeMock);
        assertTrue(eventMock.getProcessed());
        assertNull(eventMock.getReservedTo());
        assertNull(eventMock.getCleanAfter());
    }


    @Test
    void setCleanAfter() {
        LocalDateTime timeMock = LocalDateTime.now().minusMinutes(10);
        InboxEvent eventMock = InboxEvent.builder()
                .reservedTo(timeMock)
                .cleanAfter(null)
                .build();

        assertDoesNotThrow(() -> target.setCleanAfter(eventMock, timeMock));
        assertNotNull(eventMock.getCleanAfter());
        assertEquals(eventMock.getCleanAfter(), timeMock);
        assertNull(eventMock.getReservedTo());
    }
}