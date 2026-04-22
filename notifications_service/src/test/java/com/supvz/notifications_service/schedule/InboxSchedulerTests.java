package com.supvz.notifications_service.schedule;

import com.supvz.notifications_service.model.entity.EventIdTypeProjection;
import com.supvz.notifications_service.model.entity.InboxEventType;
import com.supvz.notifications_service.service.entity.InboxService;
import com.supvz.notifications_service.service.processor.InboxProcessor;
import lombok.SneakyThrows;
import org.apache.commons.lang3.reflect.FieldUtils;
import org.junit.jupiter.api.BeforeEach;
import org.junit.jupiter.api.Test;
import org.junit.jupiter.api.extension.ExtendWith;
import org.mockito.Mock;
import org.mockito.junit.jupiter.MockitoExtension;

import java.util.List;
import java.util.UUID;
import java.util.concurrent.Executor;

import static org.junit.jupiter.api.Assertions.assertDoesNotThrow;
import static org.mockito.ArgumentMatchers.anyInt;
import static org.mockito.Mockito.*;

@ExtendWith(MockitoExtension.class)
class InboxSchedulerTests {
    InboxScheduler target;
    @Mock
    Executor eventExecutor;
    @Mock
    InboxService inboxService;
    @Mock
    InboxProcessor processor;
    @Mock
    InboxEventType type;

    @SneakyThrows
    @BeforeEach
    void setUp() {
        lenient().when(processor.getType()).thenReturn(type);

        List<InboxProcessor> processorList = List.of(processor);

        target = new InboxScheduler(inboxService, eventExecutor, processorList);

        FieldUtils.writeField(target, "processingBatchSize", 1, true);
        FieldUtils.writeField(target, "cleaningBatchSize", 1, true);
    }

    @Test
    void processSuccess() {
        EventIdTypeProjection projectionMock = mock(EventIdTypeProjection.class);
        UUID eventIdMock = UUID.randomUUID();
        List<EventIdTypeProjection> batchMock = List.of(projectionMock);

        lenient().when(projectionMock.getEventId()).thenReturn(eventIdMock);
        lenient().when(projectionMock.getEventType()).thenReturn(type);

        when(inboxService.readAndReserveUnprocessedBatch(anyInt())).thenReturn(batchMock);
        doAnswer(invocation -> {
            Runnable runnable = invocation.getArgument(0);
            runnable.run();
            return null;
        }).when(eventExecutor).execute(any(Runnable.class));
        doNothing().when(processor).process(eventIdMock);

        assertDoesNotThrow(() -> target.process());

        verify(inboxService, times(1)).readAndReserveUnprocessedBatch(anyInt());
        verify(processor, times(1)).process(eventIdMock);
    }

    @Test
    void processSuccess__BatchIsEmpty() {
        List<EventIdTypeProjection> batchMock = List.of();

        when(inboxService.readAndReserveUnprocessedBatch(anyInt())).thenReturn(batchMock);

        assertDoesNotThrow(() -> target.process());

        verify(inboxService, times(1)).readAndReserveUnprocessedBatch(anyInt());
        verify(processor, never()).process(any());
    }

    @Test
    void cleanSuccess() {
        List<UUID> batchMock = List.of(UUID.randomUUID());

        when(inboxService.deleteFailedBatch(anyInt())).thenReturn(batchMock);

        assertDoesNotThrow(() -> target.clean());

        verify(inboxService, times(1)).deleteFailedBatch(anyInt());
    }
}