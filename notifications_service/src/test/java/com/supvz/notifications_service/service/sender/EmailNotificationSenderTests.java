package com.supvz.notifications_service.service.sender;

import com.supvz.notifications_service.mapper.SimpleMailMapper;
import com.supvz.notifications_service.model.dto.NotificationDto;
import com.supvz.notifications_service.model.entity.NotificationType;
import org.junit.jupiter.api.Test;
import org.junit.jupiter.api.extension.ExtendWith;
import org.mockito.InjectMocks;
import org.mockito.Mock;
import org.mockito.junit.jupiter.MockitoExtension;
import org.springframework.mail.MailException;
import org.springframework.mail.MailSendException;
import org.springframework.mail.SimpleMailMessage;
import org.springframework.mail.javamail.JavaMailSender;

import static org.junit.jupiter.api.Assertions.*;
import static org.mockito.Mockito.*;
import static org.mockito.Mockito.doThrow;
import static org.mockito.Mockito.mock;
import static org.mockito.Mockito.times;
import static org.mockito.Mockito.verify;
import static org.mockito.Mockito.when;

@ExtendWith(MockitoExtension.class)
class EmailNotificationSenderTests {
    @InjectMocks
    EmailNotificationSender target;
    @Mock
    JavaMailSender mailSender;
    @Mock
    SimpleMailMapper mapper;


    @Test
    void sendNotification__Success() {
        NotificationDto dtoMock = mock(NotificationDto.class);
        SimpleMailMessage mailMock = mock(SimpleMailMessage.class);

        when(mapper.message(dtoMock)).thenReturn(mailMock);
        doNothing().when(mailSender).send(mailMock);
        assertDoesNotThrow(() -> target.send(dtoMock));

        verify(mapper, times(1)).message(dtoMock);
        verify(mailSender, times(1)).send(mailMock);
    }

    @Test
    void sendNotification__Failed() {
        NotificationDto dtoMock = mock(NotificationDto.class);
        SimpleMailMessage mailMock = mock(SimpleMailMessage.class);

        when(mapper.message(dtoMock)).thenReturn(mailMock);
        doThrow(MailSendException.class).when(mailSender).send(mailMock);
        assertThrows(MailException.class, () -> target.send(dtoMock));

        verify(mapper, times(1)).message(dtoMock);
        verify(mailSender, times(1)).send(mailMock);
    }

    @Test
    void getType__MustBeEmail() {
        assertEquals(NotificationType.email, target.getType());
    }

}