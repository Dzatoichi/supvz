package com.supvz.notifications_service.mapper;

import com.supvz.notifications_service.model.dto.NotificationDto;
import com.supvz.notifications_service.model.dto.NotificationPayload;
import com.supvz.notifications_service.model.dto.PageDto;
import com.supvz.notifications_service.model.entity.InboxEvent;
import com.supvz.notifications_service.model.entity.Notification;
import com.supvz.notifications_service.model.entity.NotificationType;
import org.junit.jupiter.api.Test;
import org.springframework.data.domain.Page;
import org.springframework.data.domain.PageImpl;

import java.time.LocalDateTime;
import java.util.List;

import static org.assertj.core.api.Assertions.assertThat;
import static org.junit.jupiter.api.Assertions.*;
import static org.mockito.Mockito.mock;

class NotificationEntityMapperTests {
    NotificationEntityMapper target = new NotificationEntityMapper();

    @Test
    void create() {
        InboxEvent eventMock = mock(InboxEvent.class);
        NotificationType typeMock = mock(NotificationType.class);
        String subjectMock = "subjectMock";
        String bodyMock = "bodyMock";
        String recipientMock = "recipientMock";
        NotificationPayload payload = new NotificationPayload(typeMock, recipientMock, bodyMock, subjectMock);

        Notification result = assertDoesNotThrow(() -> target.create(eventMock, payload));

        assertEquals(eventMock, result.getEvent());
        assertEquals(typeMock, result.getNotificationType());
        assertEquals(bodyMock, result.getBody());
        assertEquals(subjectMock, result.getSubject());
        assertEquals(recipientMock, result.getRecipientId());
    }

    @Test
    void read() {
        long idMock = 1;
        String bodyMock = "bodyMock";
        String subjectMock = "subjectMock";
        String recipientIdMock = "recipientId";
        boolean viewedMock = true;
        LocalDateTime sentAtMock = LocalDateTime.now().minusMinutes(1);
        NotificationType typeMock = mock(NotificationType.class);

        Notification notificationMock = Notification.builder()
                .id(idMock)
                .notificationType(typeMock)
                .subject(subjectMock)
                .recipientId(recipientIdMock)
                .sentAt(sentAtMock)
                .viewed(viewedMock)
                .body(bodyMock)
                .build();

        NotificationDto result = assertDoesNotThrow(() -> target.read(notificationMock));
        assertEquals(idMock, result.id());
        assertEquals(typeMock, result.notificationType());
        assertEquals(subjectMock, result.subject());
        assertEquals(recipientIdMock, result.recipientId());
        assertEquals(sentAtMock, result.sentAt());
        assertEquals(viewedMock, result.viewed());
        assertEquals(bodyMock, result.body());
    }

    @Test
    void markAsSentSuccess() {
        Notification entityMock = Notification.builder()
                .sent(false)
                .build();

        assertDoesNotThrow(() -> target.markAsSent(entityMock));

        assertNotNull(entityMock.getSentAt());
        assertTrue(entityMock.getSent());
    }

    @Test
    void markAsSentFailed() {
        LocalDateTime sentAtMock = LocalDateTime.now().minusMinutes(10);
        boolean sentMock = true;
        Notification entityMock = Notification.builder()
                .sent(sentMock)
                .sentAt(sentAtMock)
                .build();

        assertDoesNotThrow(() -> target.markAsSent(entityMock));

        assertSame(sentAtMock, entityMock.getSentAt());
        assertSame(sentMock, entityMock.getSent());
    }

    @Test
    void readPage() {
        Notification notification1 = Notification.builder()
                .id(1L)
                .recipientId("user1")
                .body("Test body 1")
                .subject("Test subject 1")
                .sentAt(LocalDateTime.now())
                .sent(true)
                .viewed(false)
                .createdAt(LocalDateTime.now().minusDays(1))
                .updatedAt(LocalDateTime.now())
                .build();
        Notification notification2 = Notification.builder()
                .id(2L)
                .recipientId("user2")
                .body("Test body 2")
                .subject("Test subject 2")
                .sentAt(LocalDateTime.now())
                .sent(false)
                .viewed(true)
                .createdAt(LocalDateTime.now().minusHours(2))
                .updatedAt(LocalDateTime.now())
                .build();
        List<Notification> content = List.of(notification1, notification2);
        Page<Notification> page = new PageImpl<>(content);

        PageDto<NotificationDto> result = assertDoesNotThrow(() -> target.readPage(page));
        NotificationDto dto1 = result.content().get(0);
        NotificationDto dto2 = result.content().get(1);

        assertThat(result.content()).hasSize(2);
        assertThat(result.page()).isEqualTo(0);
        assertThat(result.size()).isEqualTo(2);
        assertThat(result.total()).isEqualTo(1);
        assertThat(result.hasNext()).isFalse();
        assertThat(result.hasPrev()).isFalse();
        assertThat(dto1).isNotNull();
        assertThat(dto2).isNotNull();
        assertThat(dto1.recipientId()).isEqualTo("user1");
        assertThat(dto2.recipientId()).isEqualTo("user2");
    }
}