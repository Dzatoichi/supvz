package com.supvz.requests_service.entity;

import jakarta.persistence.*;
import lombok.*;

import java.util.ArrayList;
import java.util.List;
import java.util.UUID;

@Entity
@Table(name = "requests")
@Builder
@AllArgsConstructor
@NoArgsConstructor
@Getter
@Setter
/*
Сущность запроса мастеру.
 */
public class Request {
    @Id
    @GeneratedValue(strategy = GenerationType.IDENTITY)
    private Long id;

    private int pvzId;

    private UUID appellantId;

    private String description;

    @OneToMany(mappedBy = "request", cascade = CascadeType.ALL, orphanRemoval = true)
    private List<RequestAssignment> assignments = new ArrayList<>();

    @Override
    public boolean equals(Object obj) {
        if (obj == this) return true;

        if (!(obj instanceof Request request)) return false;

        if (id == null || request.id == null) {
            return false;
        }

        return id.equals(request.id);
    }

    @Override
    public int hashCode() {
        return id == null ? System.identityHashCode(this) : id.hashCode();
    }
}