package com.supvz.notifications_service.service.entity;

import com.supvz.notifications_service.core.exception.NotificationConflictException;
import com.supvz.notifications_service.core.exception.NotificationIsNotSentException;
import com.supvz.notifications_service.core.exception.NotificationNotFoundException;
import com.supvz.notifications_service.core.filter.NotificationFilter;
import com.supvz.notifications_service.mapper.NotificationMapper;
import com.supvz.notifications_service.model.dto.NotificationDto;
import com.supvz.notifications_service.model.dto.NotificationPayload;
import com.supvz.notifications_service.model.dto.PageDto;
import com.supvz.notifications_service.model.entity.InboxEvent;
import com.supvz.notifications_service.model.entity.Notification;
import com.supvz.notifications_service.model.entity.NotificationType;
import com.supvz.notifications_service.repo.NotificationRepository;
import com.supvz.notifications_service.service.sender.NotificationSender;
import lombok.SneakyThrows;
import org.apache.commons.lang3.reflect.FieldUtils;
import org.junit.jupiter.api.BeforeEach;
import org.junit.jupiter.api.Test;
import org.junit.jupiter.api.extension.ExtendWith;
import org.mockito.Mock;
import org.mockito.junit.jupiter.MockitoExtension;
import org.springframework.beans.factory.annotation.Value;
import org.springframework.cglib.core.ReflectUtils;
import org.springframework.data.domain.Page;
import org.springframework.data.domain.PageRequest;
import org.springframework.data.domain.Pageable;
import org.springframework.data.jpa.domain.Specification;

import java.lang.reflect.Field;
import java.util.Arrays;
import java.util.List;
import java.util.Optional;
import java.util.UUID;

import static org.junit.jupiter.api.Assertions.*;
import static org.mockito.Mockito.*;

@ExtendWith(MockitoExtension.class)
class NotificationEntityServiceTests {
    NotificationEntityService target;
    @Mock
    NotificationMapper mapper;
    @Mock
    NotificationRepository repo;
    @Mock
    NotificationSender sender;
    @Mock
    NotificationType type;

    @BeforeEach
    void setUp() {
        lenient().when(sender.getType()).thenReturn(type);

        List<NotificationSender> senderList = List.of(sender);
        target = new NotificationEntityService(mapper, repo, senderList);
    }

    @Test
    void createSuccess() {
        InboxEvent eventMock = mock(InboxEvent.class);
        NotificationPayload payloadMock = mock(NotificationPayload.class);
        Notification mapped = mock(Notification.class);
        Notification saved = mock(Notification.class);

        when(mapper.create(eventMock, payloadMock)).thenReturn(mapped);
        when(repo.save(mapped)).thenReturn(saved);

        assertDoesNotThrow(() -> target.create(eventMock, payloadMock));

        verify(mapper, times(1)).create(eventMock, payloadMock);
        verify(repo, times(1)).save(mapped);
    }

    @Test
    void findAllSuccess() {
        int pageNumberMock = 1;
        int sizeMock = 1;
        Pageable pageableMock = PageRequest.of(pageNumberMock, sizeMock);
        NotificationFilter filterMock = mock(NotificationFilter.class);
        Page<Notification> pageMock = mock(Page.class);
        PageDto<NotificationDto> dtoPageMock = mock(PageDto.class);

        when(repo.findAll(any(Specification.class), eq(pageableMock))).thenReturn(pageMock);
        when(mapper.readPage(pageMock)).thenReturn(dtoPageMock);

        PageDto<NotificationDto> result = assertDoesNotThrow(
                () -> target.findAll(pageNumberMock, sizeMock, filterMock));
        assertEquals(dtoPageMock, result);

        verify(repo, times(1)).findAll(any(Specification.class), eq(pageableMock));
        verify(mapper, times(1)).readPage(pageMock);
    }

    @Test
    void processByEventIdSuccess() {
        UUID eventIdMock = UUID.randomUUID();
        Notification notificationMock = mock(Notification.class);
        NotificationDto notificationDtoMock = NotificationDto.builder().notificationType(type).build();

        when(repo.findByEventId(eventIdMock)).thenReturn(Optional.of(notificationMock));
        when(mapper.read(notificationMock)).thenReturn(notificationDtoMock);
        doNothing().when(sender).send(notificationDtoMock);

        assertDoesNotThrow(() -> target.processByEventId(eventIdMock));

        verify(repo, times(1)).findByEventId(eventIdMock);
        verify(mapper, times(1)).read(notificationMock);
        verify(sender, times(1)).send(notificationDtoMock);
        verify(mapper, times(1)).markAsSent(notificationMock);
        verify(repo, times(1)).save(notificationMock);
    }

    @Test
    void processByEventIdFailed__UnhandledType() {
        UUID eventIdMock = UUID.randomUUID();
        Notification notificationMock = mock(Notification.class);
        NotificationDto notificationDtoMock = mock(NotificationDto.class);

        when(repo.findByEventId(eventIdMock)).thenReturn(Optional.of(notificationMock));
        when(mapper.read(notificationMock)).thenReturn(notificationDtoMock);

        assertThrows(NotificationIsNotSentException.class, () -> target.processByEventId(eventIdMock));

        verify(repo, times(1)).findByEventId(eventIdMock);
        verify(mapper, times(1)).read(notificationMock);
        verify(sender, never()).send(any());
        verify(mapper, never()).markAsSent(any());
        verify(repo, never()).save(any());
    }

    @Test
    void processByEventIdFailed__ExceptionWhileSending() {
        UUID eventIdMock = UUID.randomUUID();
        Notification notificationMock = mock(Notification.class);
        NotificationDto notificationDtoMock = NotificationDto.builder().notificationType(type).build();

        when(repo.findByEventId(eventIdMock)).thenReturn(Optional.of(notificationMock));
        when(mapper.read(notificationMock)).thenReturn(notificationDtoMock);
        doThrow(RuntimeException.class).when(sender).send(notificationDtoMock);

        assertThrows(NotificationIsNotSentException.class, () -> target.processByEventId(eventIdMock));

        verify(repo, times(1)).findByEventId(eventIdMock);
        verify(mapper, times(1)).read(notificationMock);
        verify(sender, times(1)).send(notificationDtoMock);
        verify(mapper, never()).markAsSent(any());
        verify(repo, never()).save(any());
    }

    @Test
    void processByEventIdFailed__NotificationNotFound() {
        UUID eventIdMock = UUID.randomUUID();

        when(repo.findByEventId(eventIdMock)).thenReturn(Optional.empty());

        assertThrows(NotificationNotFoundException.class, () -> target.processByEventId(eventIdMock));

        verify(repo, times(1)).findByEventId(eventIdMock);
        verify(mapper, never()).read(any());
        verify(sender, never()).send(any());
        verify(mapper, never()).markAsSent(any());
        verify(repo, never()).save(any());
    }

    @Test
    void processByEventIdFailed__AlreadySent() {
        UUID eventIdMock = UUID.randomUUID();
        Notification notificationMock = Notification.builder().sent(true).build();
        NotificationDto notificationDtoMock = mock(NotificationDto.class);

        when(repo.findByEventId(eventIdMock)).thenReturn(Optional.of(notificationMock));
        when(mapper.read(notificationMock)).thenReturn(notificationDtoMock);

        assertThrows(NotificationConflictException.class, () -> target.processByEventId(eventIdMock));

        verify(repo, times(1)).findByEventId(eventIdMock);
        verify(mapper, times(1)).read(notificationMock);
        verify(sender, never()).send(any());
        verify(mapper, never()).markAsSent(any());
        verify(repo, never()).save(any());
    }

    @Test
    @SneakyThrows
    void deleteOldNotificationsSuccess() {
        List<Integer> listMock = List.of();
        FieldUtils.writeField(target, "emailTtlDays", 1, true);
        FieldUtils.writeField(target, "viewedTtlDays", 1, true);
        FieldUtils.writeField(target, "notViewedTtlDays", 1, true);

        when(repo.deleteOldNotifications(any(Integer.class),
                any(Integer.class), any(Integer.class))).thenReturn(listMock);

        List<Integer> result = assertDoesNotThrow(() -> target.deleteOldNotifications());
        assertEquals(listMock, result);

        verify(repo, times(1)).deleteOldNotifications(
                any(Integer.class), any(Integer.class), any(Integer.class));
    }
}