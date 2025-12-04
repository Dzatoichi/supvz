package com.supvz.notifications_service.service.sender;

import com.supvz.notifications_service.model.dto.NotificationDto;
import com.supvz.notifications_service.model.entity.NotificationType;
import org.junit.jupiter.api.Test;
import org.junit.jupiter.api.extension.ExtendWith;
import org.mockito.InjectMocks;
import org.mockito.junit.jupiter.MockitoExtension;

import static org.junit.jupiter.api.Assertions.*;
import static org.mockito.Mockito.mock;

@ExtendWith(MockitoExtension.class)
class PushNotificationSenderTests {
    @InjectMocks
    PushNotificationSender target;

    @Test
    void sendSuccess() {
        NotificationDto notificationMock = mock(NotificationDto.class);

        assertDoesNotThrow(() -> target.send(notificationMock));
    }

    @Test
    void getTypeShouldReturnPushType() {
        assertEquals(NotificationType.push, target.getType());
    }

}