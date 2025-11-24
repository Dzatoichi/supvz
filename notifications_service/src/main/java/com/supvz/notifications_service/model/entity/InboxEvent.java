package com.supvz.notifications_service.model.entity;

import jakarta.persistence.*;
import lombok.*;
import org.hibernate.annotations.JdbcType;
import org.hibernate.dialect.PostgreSQLEnumJdbcType;

import java.time.LocalDateTime;
import java.util.UUID;

@Table(name = "inbox")
@Entity
@Getter
@Setter
@Builder
@AllArgsConstructor
@NoArgsConstructor
public class InboxEvent {
    @Id
    private UUID eventId;

    @JdbcType(PostgreSQLEnumJdbcType.class)
    @Column(name = "event_type")
    private InboxEventType eventType;

    private String payload;

    private LocalDateTime reservedTo;

    private LocalDateTime createdAt;

    private LocalDateTime updatedAt;

    private LocalDateTime processedAt;

    private Boolean processed;

    private LocalDateTime cleanAfter;

    @PrePersist
    private void prePersist() {
        if (createdAt == null) createdAt = LocalDateTime.now();
        if (processed == null) processed = false;
    }

    @Override
    public boolean equals(Object o) {
        if (o == this) return true;

        if (!(o instanceof InboxEvent event)) return false;

        if (eventId == null || event.eventId == null) return false;

        return eventId.equals(event.eventId);
    }

    @Override
    public int hashCode() {
        return eventId == null ? System.identityHashCode(this) : eventId.hashCode();
    }
}