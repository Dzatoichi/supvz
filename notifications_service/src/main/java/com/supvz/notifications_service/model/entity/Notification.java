package com.supvz.notifications_service.model.entity;

import jakarta.persistence.*;
import lombok.*;

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
    @Column(name = "notification_type")
    @Enumerated(EnumType.STRING)
    private NotificationType notificationType;
    private String recipientId;
    private String body;
    private String subject;
    private LocalDateTime sentAt;
    private Boolean sent;
    private Boolean viewed;
    private LocalDateTime createdAt;
    private LocalDateTime updatedAt;

    //    todo: реализовать updated_at
//          есть какая то реализация от спринга

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

    @PrePersist
    private void prePersist() {
        if (createdAt == null) createdAt = LocalDateTime.now();
        if (updatedAt == null) updatedAt = LocalDateTime.now();
        if (sent == null) sent = false;
    }
}