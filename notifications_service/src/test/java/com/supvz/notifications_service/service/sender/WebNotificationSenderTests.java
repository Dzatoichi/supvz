package com.supvz.notifications_service.service.sender;

import com.fasterxml.jackson.databind.ObjectMapper;
import com.supvz.notifications_service.model.dto.NotificationDto;
import lombok.SneakyThrows;
import org.apache.commons.lang3.reflect.FieldUtils;
import org.junit.jupiter.api.BeforeEach;
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

    @BeforeEach
    void setUp() throws IllegalAccessException {
        FieldUtils.writeField(target, "baseTopic", "valueMock", true);
    }

    @SneakyThrows
    @Test
    void sendWebNotification__Success() {
        NotificationDto mockDto = NotificationDto.builder().recipientId("recipientIdMock").build();
        String mockSerialized = "serializedMock";

        when(objectMapper.writeValueAsString(mockDto)).thenReturn(mockSerialized);
        doNothing().when(messagingTemplate).convertAndSend(any(String.class), eq(mockSerialized));

        assertDoesNotThrow(() -> target.send(mockDto));

        verify(objectMapper, times(1)).writeValueAsString(mockDto);
        verify(messagingTemplate, times(1)).convertAndSend(any(String.class), eq(mockSerialized));
    }
}