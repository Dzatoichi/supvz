package com.supvz.notifications_service.service.sender;

import com.fasterxml.jackson.databind.ObjectMapper;
import com.supvz.notifications_service.model.dto.NotificationDto;
import lombok.SneakyThrows;
import org.junit.jupiter.api.Test;
import org.junit.jupiter.api.extension.ExtendWith;
import org.mockito.InjectMocks;
import org.mockito.Mock;
import org.mockito.junit.jupiter.MockitoExtension;
import org.springframework.messaging.simp.SimpMessagingTemplate;

import static org.junit.jupiter.api.Assertions.*;
import static org.mockito.ArgumentMatchers.any;
import static org.mockito.Mockito.*;
import static org.mockito.Mockito.times;
import static org.mockito.Mockito.verify;

@ExtendWith(MockitoExtension.class)
class WebNotificationSenderTests {
    @InjectMocks
    WebNotificationSender target;
    @Mock
    SimpMessagingTemplate messagingTemplate;
    @Mock
    ObjectMapper objectMapper;

    @SneakyThrows
    @Test
    void sendWebNotification__Success() {
        NotificationDto mockDto = mock(NotificationDto.class);
        String mockSerialized = "serializedMock";
        String mockDestination = "dummy";

        when(objectMapper.writeValueAsString(mockDto)).thenReturn(mockSerialized);
        doNothing().when(messagingTemplate).convertAndSend(mockDestination, mockSerialized);

        assertDoesNotThrow(() -> target.send(mockDto));

        verify(objectMapper, times(1)).writeValueAsString(mockDto);
        verify(messagingTemplate, times(1)).convertAndSend(any(), mockSerialized);
    }
}