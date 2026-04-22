package com.supvz.notifications_service.service.entity;

import com.supvz.notifications_service.core.exception.InboxEventConflictException;
import com.supvz.notifications_service.core.exception.InboxEventNotFoundException;
import com.supvz.notifications_service.mapper.InboxMapper;
import com.supvz.notifications_service.model.dto.InboxMessage;
import com.supvz.notifications_service.model.entity.EventIdTypeProjection;
import com.supvz.notifications_service.model.entity.InboxEvent;
import com.supvz.notifications_service.model.entity.InboxEventType;
import com.supvz.notifications_service.repo.InboxEventRepository;
import org.junit.jupiter.api.Test;
import org.junit.jupiter.api.extension.ExtendWith;
import org.mockito.InjectMocks;
import org.mockito.Mock;
import org.mockito.junit.jupiter.MockitoExtension;

import java.time.LocalDateTime;
import java.util.List;
import java.util.Optional;
import java.util.UUID;

import static org.junit.jupiter.api.Assertions.*;
import static org.mockito.Mockito.*;

@ExtendWith(MockitoExtension.class)
class InboxEntityServiceTests {
    @InjectMocks
    InboxEntityService target;
    @Mock
    InboxEventRepository repo;
    @Mock
    InboxMapper mapper;

    @Test
    void createSuccess() {
        InboxMessage messageMock = mock(InboxMessage.class);
        InboxEvent mappedMock = InboxEvent.builder().eventType(InboxEventType.notification).build();
        InboxEvent savedMock = mock(InboxEvent.class);

        when(mapper.create(messageMock)).thenReturn(mappedMock);
        when(repo.saveIfNotExists(mappedMock.getEventId(),
                mappedMock.getEventType().name(),
                mappedMock.getPayload()))
                .thenReturn(savedMock);

        InboxEvent result = assertDoesNotThrow(() -> target.create(messageMock));
        assertEquals(savedMock, result);

        verify(mapper, times(1)).create(messageMock);
        verify(repo, times(1)).saveIfNotExists(mappedMock.getEventId(),
                mappedMock.getEventType().name(),
                mappedMock.getPayload());
    }

    @Test
    void createFailed__Conflict() {
        InboxMessage messageMock = mock(InboxMessage.class);
        InboxEvent mappedMock = InboxEvent.builder().eventType(InboxEventType.notification).build();

        when(mapper.create(messageMock)).thenReturn(mappedMock);
        when(repo.saveIfNotExists(mappedMock.getEventId(),
                mappedMock.getEventType().name(),
                mappedMock.getPayload()))
                .thenReturn(null);

        assertThrows(InboxEventConflictException.class,
                () -> target.create(messageMock));

        verify(mapper, times(1)).create(messageMock);
        verify(repo, times(1)).saveIfNotExists(mappedMock.getEventId(),
                mappedMock.getEventType().name(),
                mappedMock.getPayload());
    }

    @Test
    void readAndReserveSuccess() {
        int batchSize = 1;
        List<EventIdTypeProjection> eventsMock = List.of();

        when(repo.findAndReserveUnprocessedInBatch(eq(batchSize), any(LocalDateTime.class)))
                .thenReturn(eventsMock);

        List<EventIdTypeProjection> result = assertDoesNotThrow(
                () -> target.readAndReserveUnprocessedBatch(batchSize));

        assertEquals(eventsMock, result);

        verify(repo, times(1))
                .findAndReserveUnprocessedInBatch(eq(batchSize), any(LocalDateTime.class));
    }

    @Test
    void setProcessedSuccess() {
        UUID eventIdMock = UUID.randomUUID();
        InboxEvent eventMock = mock(InboxEvent.class);

        when(repo.findById(eventIdMock)).thenReturn(Optional.of(eventMock));
        doNothing().when(mapper).markAsProcessed(eventMock);

        assertDoesNotThrow(() -> target.setProcessed(eventIdMock));

        verify(repo, times(1)).findById(eventIdMock);
        verify(mapper, times(1)).markAsProcessed(eventMock);
        verify(repo, times(1)).save(eventMock);
    }

    @Test
    void setProcessedFailed__EventNotFound() {
        UUID eventIdMock = UUID.randomUUID();

        when(repo.findById(eventIdMock)).thenReturn(Optional.empty());

        assertThrows(InboxEventNotFoundException.class, () -> target.setProcessed(eventIdMock));

        verify(repo, times(1)).findById(eventIdMock);
        verify(mapper, never()).markAsProcessed(any(InboxEvent.class));
        verify(repo, never()).save(any(InboxEvent.class));
    }

    @Test
    void setProcessedFailed__AlreadyProcessed() {
        UUID eventIdMock = UUID.randomUUID();
        InboxEvent eventMock = InboxEvent.builder().processed(true).build();

        when(repo.findById(eventIdMock)).thenReturn(Optional.of(eventMock));

        assertDoesNotThrow(() -> target.setProcessed(eventIdMock));

        verify(repo, times(1)).findById(eventIdMock);
        verify(mapper, never()).markAsProcessed(any(InboxEvent.class));
        verify(repo, never()).save(any(InboxEvent.class));
    }

    @Test
    void cleanAfterSuccess() {
        UUID eventIdMock = UUID.randomUUID();
        InboxEvent eventMock = mock(InboxEvent.class);

        when(repo.findById(eventIdMock)).thenReturn(Optional.of(eventMock));
        doNothing().when(mapper).setCleanAfter(eq(eventMock), any(LocalDateTime.class));

        assertDoesNotThrow(() -> target.setCleanAfter(eventIdMock));

        verify(repo, times(1)).findById(eventIdMock);
        verify(mapper, times(1))
                .setCleanAfter(eq(eventMock), any(LocalDateTime.class));
        verify(repo, times(1)).save(eventMock);
    }


    @Test
    void cleanAfterFailed__EventNotFound() {
        UUID eventIdMock = UUID.randomUUID();

        when(repo.findById(eventIdMock)).thenReturn(Optional.empty());

        assertThrows(InboxEventNotFoundException.class, () -> target.setCleanAfter(eventIdMock));

        verify(repo, times(1)).findById(eventIdMock);
        verify(mapper, never())
                .setCleanAfter(any(), any());
        verify(repo, never()).save(any());
    }

    @Test
    void cleanAfterFailed__AlreadySetCleaned() {
        UUID eventIdMock = UUID.randomUUID();
        InboxEvent eventMock = InboxEvent.builder().cleanAfter(LocalDateTime.now()).build();

        when(repo.findById(eventIdMock)).thenReturn(Optional.of(eventMock));

        assertDoesNotThrow(() -> target.setCleanAfter(eventIdMock));

        verify(repo, times(1)).findById(eventIdMock);
        verify(mapper, never())
                .setCleanAfter(eq(eventMock), any(LocalDateTime.class));
        verify(repo, never()).save(eventMock);
    }

    @Test
    void deleteFailedBatchSuccess() {
        int batchSizeMock = 1;
        List<UUID> listMock = List.of();

        when(repo.deleteFailedInBatch(batchSizeMock)).thenReturn(listMock);

        List<UUID> result = assertDoesNotThrow(() -> target.deleteFailedBatch(batchSizeMock));
        assertEquals(listMock, result);

        verify(repo, times(1)).deleteFailedInBatch(batchSizeMock);

    }

}