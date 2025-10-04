package com.supvz.requests_service.mapper.impl;

import com.supvz.requests_service.core.*;
import com.supvz.requests_service.entity.Request;
import com.supvz.requests_service.entity.RequestAssignment;
import com.supvz.requests_service.mapper.RequestAssignmentMapper;
import org.springframework.data.domain.Page;
import org.springframework.stereotype.Component;

import java.time.LocalDateTime;
import java.util.UUID;

@Component
public class RequestAssignmentMapperImpl implements RequestAssignmentMapper {
    @Override
    public RequestAssignment create(Request request, RequestAssignmentPayload payload) {
        return RequestAssignment.builder()
                .request(request)
                .handymanId(payload.handymanId())
                .description(payload.description())
                .build();
    }

    @Override
    public RequestAssignmentDto read(RequestAssignment assignment) {
        return RequestAssignmentDto
                .builder()
                .id(assignment.getId())
                .assignedAt(assignment.getAssignedAt())
                .status(assignment.getStatus())
                .handymanId(assignment.getHandymanId())
                .completedAt(assignment.getCompletedAt())
                .description(assignment.getDescription())
                .requestId(assignment.getRequest().getId())
                .build();
    }

    @Override
    public PageDto<RequestAssignmentDto> readPage(Page<RequestAssignment> page) {
        return PageDto.<RequestAssignmentDto>builder()
                .content(page.getContent().stream().map(this::read).toList())
                .page(page.getNumber())
                .size(page.getSize())
                .total(page.getTotalPages())
                .hasNext(page.hasNext())
                .hasPrev(page.hasPrevious())
                .build();
    }

    @Override
    public RequestAssignment update(RequestAssignment assignment, RequestAssignmentUpdatePayload payload) {
        UUID handymanId = payload.handymanId();
        Status status = payload.status();
        String description = payload.description();

        if (handymanId != null)
            assignment.setHandymanId(handymanId);

        if (status != null) {
            assignment.setStatus(status);
            switch (status) {
                case Status.CONFIRMED:
                    assignment.setCompletedAt(LocalDateTime.now());
                case Status.REJECTED:
                    assignment.setCompletedAt(LocalDateTime.now());
            }
        }

        if (description != null)
            assignment.setDescription(description);

        return assignment;
    }
}
