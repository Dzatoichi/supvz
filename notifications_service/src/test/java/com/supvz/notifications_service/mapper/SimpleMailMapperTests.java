package com.supvz.notifications_service.mapper;

import com.supvz.notifications_service.model.dto.NotificationDto;
import lombok.SneakyThrows;
import org.apache.commons.lang3.reflect.FieldUtils;
import org.junit.jupiter.api.BeforeEach;
import org.junit.jupiter.api.Test;
import org.junit.jupiter.api.extension.ExtendWith;
import org.mockito.InjectMocks;
import org.mockito.junit.jupiter.MockitoExtension;
import org.springframework.mail.SimpleMailMessage;

import static org.junit.jupiter.api.Assertions.*;

@ExtendWith(MockitoExtension.class)
class SimpleMailMapperTests {
    @InjectMocks
    SimpleMailMapper target;

    @BeforeEach
    @SneakyThrows
    void setUp() {
        FieldUtils.writeField(target, "from", "fromMock", true);
    }

    @Test
    void messageSuccess() {
        String bodyMock = "bodyMock";
        String recipientIdMock = "recipientIdMock";
        String subjectMock = "subjectMock";
        NotificationDto notificationMock = NotificationDto.builder()
                .subject(subjectMock)
                .recipientId(recipientIdMock)
                .body(bodyMock)
                .build();

        SimpleMailMessage result = assertDoesNotThrow(() -> target.message(notificationMock));

        assertEquals(bodyMock, result.getText());
        assertNotNull(result.getTo());
        assertEquals(recipientIdMock, result.getTo()[0]);
        assertEquals(subjectMock, result.getSubject());
    }



}