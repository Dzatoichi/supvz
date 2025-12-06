package com.supvz.requests_service.model.entity;

import com.supvz.requests_service.core.enums.AssignmentAction;
import com.supvz.requests_service.core.enums.RequestStatus;
import jakarta.persistence.*;
import lombok.*;
import org.hibernate.annotations.CreationTimestamp;

import java.time.LocalDateTime;

@Entity
@Table(name = "request_assignments")
@Builder
@AllArgsConstructor
@NoArgsConstructor
@Getter
@Setter
public class RequestAssignment {
    @Id
    @GeneratedValue(strategy = GenerationType.IDENTITY)
    private Long id;

    @ManyToOne
    @JoinColumn(name = "request_id", nullable = false)
    private Request request;

    private long handymanId;

    @Enumerated(EnumType.STRING)
    private AssignmentAction action;

    private LocalDateTime processedAt;

    private String comment;

    private LocalDateTime createdAt;

    private LocalDateTime updatedAt;


    @PrePersist
    private void prePersist() {
        if (createdAt == null) createdAt = LocalDateTime.now();
        if (updatedAt == null) updatedAt = LocalDateTime.now();
        if (action == null) action = AssignmentAction.assign;
    }

    @PreUpdate
    private void preUpdate() {
        updatedAt = LocalDateTime.now();
    }

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
}