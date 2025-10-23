package com.supvz.requests_service.entity;

import com.supvz.requests_service.core.Status;
import jakarta.persistence.*;
import lombok.*;
import org.hibernate.annotations.CreationTimestamp;

import java.time.LocalDateTime;
import java.util.UUID;

@Entity
@Table(name = "request_assignments")
@Builder
@AllArgsConstructor
@NoArgsConstructor
@Getter
@Setter
/*
Сущность ответа на запрос.
 */
public class RequestAssignment {
    @Id
    @GeneratedValue(strategy = GenerationType.IDENTITY)
    private Long id;

    @ManyToOne
    @JoinColumn(name = "request_id", nullable = false)
    private Request request;

    private UUID handymanId;

    @Enumerated(EnumType.STRING)
    private Status status;

    @CreationTimestamp
    private LocalDateTime assignedAt;

    private LocalDateTime completedAt;

    private String description;

    @Override
    public boolean equals(Object obj) {
        if (obj == this) return true;

        if (!(obj instanceof RequestAssignment assignment)) return false;

        if (id == null || assignment.id == null) {
            return false;
        }

        return id.equals(assignment.id);
    }

    @Override
    public int hashCode() {
        return id == null ? System.identityHashCode(this) : id.hashCode();
    }

    @PrePersist
    private void prePersist() {
        if (status == null) status = Status.ASSIGNED;
    }
}