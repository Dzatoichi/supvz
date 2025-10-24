package com.supvz.notifications_service.entity;

import jakarta.persistence.*;
import lombok.*;
import org.hibernate.annotations.CreationTimestamp;
import org.hibernate.annotations.JdbcType;
import org.hibernate.dialect.PostgreSQLEnumJdbcType;

import java.time.LocalDateTime;

@Table(name = "notifications")
@Entity
@Getter
@Setter
@AllArgsConstructor
@NoArgsConstructor
@Builder
public class Notification {
    @Id
    @GeneratedValue(strategy = GenerationType.IDENTITY)
    private Long id;

    @OneToOne(fetch = FetchType.LAZY)
    @JoinColumn(name = "event_id")
    private InboxEvent event;

    @JdbcType(PostgreSQLEnumJdbcType.class)
    @Column(name = "notification_type")
    private NotificationType notificationType;

    private String recipientId;

    private String body;

    private String subject;

    @CreationTimestamp
    private LocalDateTime createdAt;

    private LocalDateTime sentAt;


    @Override
    public boolean equals(Object o) {
        if (o == this) return true;

        if (!(o instanceof Notification notification)) return false;

        if (id == null || notification.id == null) return false;

        return id.equals(notification.id);
    }

    @Override
    public int hashCode() {
        return id == null ? System.identityHashCode(this) : id.hashCode();
    }
}
