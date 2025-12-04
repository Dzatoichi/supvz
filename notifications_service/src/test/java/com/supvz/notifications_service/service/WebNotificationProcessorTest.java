package com.supvz.notifications_service.service;

import com.fasterxml.jackson.databind.ObjectMapper;
import com.supvz.notifications_service.model.dto.NotificationDto;
import com.supvz.notifications_service.service.impl.WebNotificationProcessor;
import lombok.SneakyThrows;
import org.junit.jupiter.api.Assertions;
import org.junit.jupiter.api.Test;
import org.junit.jupiter.api.extension.ExtendWith;
import org.junit.platform.commons.util.ReflectionUtils;
import org.mockito.InjectMocks;
import org.mockito.Mock;
import org.mockito.junit.jupiter.MockitoExtension;
import org.springframework.boot.test.context.SpringBootTest;
import org.springframework.messaging.simp.SimpMessagingTemplate;

import static org.junit.jupiter.api.Assertions.assertDoesNotThrow;
import static org.mockito.Mockito.*;

@ExtendWith(MockitoExtension.class)
//@SpringBootTest(webEnvironment = SpringBootTest.WebEnvironment.MOCK)
class WebNotificationProcessorTest {
    @InjectMocks
    WebNotificationProcessor target;
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