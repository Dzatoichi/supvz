package com.supvz.requests_service.mapper;

import com.supvz.requests_service.core.enums.AssignmentAction;
import com.supvz.requests_service.model.dto.PageDto;
import com.supvz.requests_service.model.dto.RequestAssignmentDto;
import com.supvz.requests_service.model.dto.RequestAssignmentPayload;
import com.supvz.requests_service.model.dto.RequestAssignmentUpdatePayload;
import com.supvz.requests_service.model.entity.Request;
import com.supvz.requests_service.model.entity.RequestAssignment;
import org.springframework.data.domain.Page;
import org.springframework.stereotype.Component;

/**
 * Реализация маппера для работы с ответами на заявки.
 */
@Component
public class RequestAssignmentEntityMapper implements RequestAssignmentMapper {

    /**
     * Метод для преобразования полезной нагрузки в сущность.
     */
    @Override
    public RequestAssignment create(Request request, RequestAssignmentPayload payload) {
        return RequestAssignment.builder()
                .request(request)
                .handymanId(payload.handymanId())
                .comment(payload.comment())
                .build();
    }

    /**
     * Метод для преобразования сущности в ДТО.
     */
    @Override
    public RequestAssignmentDto read(RequestAssignment assignment) {
        return new RequestAssignmentDto(
                assignment.getId(),
                assignment.getRequest().getId(),
                assignment.getHandymanId(),
                assignment.getAction(),
                assignment.getProcessedAt(),
                assignment.getCreatedAt(),
                assignment.getUpdatedAt(),
                assignment.getComment()
        );
    }

    /**
     * Метод для преобразования Page из springframework.data.Page в ДТО
     */
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

    /**
     * Метод для преобразования сущности и полезной нагрузки для обновления в сущность.
     */
    @Override
    public RequestAssignment update(RequestAssignment assignment, RequestAssignmentUpdatePayload payload) {
        Long handymanId = payload.handymanId();
        String comment = payload.comment();
        if (handymanId != null)
            assignment.setHandymanId(handymanId);
        if (comment != null)
            assignment.setComment(comment);
        return assignment;
    }
}
