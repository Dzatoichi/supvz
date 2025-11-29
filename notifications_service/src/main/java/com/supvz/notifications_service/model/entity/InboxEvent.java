package com.supvz.notifications_service.model.entity;

import jakarta.persistence.*;
import lombok.*;

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
    @Enumerated(EnumType.STRING)
    @Column(name = "event_type")
    private InboxEventType eventType;
    private String payload;
    private LocalDateTime reservedTo;
    private LocalDateTime processedAt;
    private Boolean processed;
    private LocalDateTime cleanAfter;
    private LocalDateTime createdAt;
    private LocalDateTime updatedAt;

    @PrePersist
    private void prePersist() {
        if (createdAt == null) createdAt = LocalDateTime.now();
        if (updatedAt == null) createdAt = LocalDateTime.now();
        if (processed == null) processed = false;
    }

    @PreUpdate
    private void preUpdate() {
        updatedAt = LocalDateTime.now();
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