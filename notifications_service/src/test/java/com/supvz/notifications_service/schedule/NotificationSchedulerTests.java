package com.supvz.notifications_service.schedule;

import com.supvz.notifications_service.service.entity.NotificationService;
import org.junit.jupiter.api.Test;
import org.junit.jupiter.api.extension.ExtendWith;
import org.mockito.InjectMocks;
import org.mockito.Mock;
import org.mockito.junit.jupiter.MockitoExtension;

import java.util.List;

import static org.junit.jupiter.api.Assertions.*;
import static org.mockito.Mockito.when;

@ExtendWith(MockitoExtension.class)
class NotificationSchedulerTests {
    @InjectMocks
    NotificationScheduler target;
    @Mock
    NotificationService notificationService;

    @Test
    void pollingForCleaningOldNotificationsSuccess() {
        List<Integer> batchMock = List.of(1);

        when(notificationService.deleteOldNotifications()).thenReturn(batchMock);

        assertDoesNotThrow(() -> target.pollingForCleaningOldNotifications());
    }
}