package com.supvz.requests_service.mapper.entity;

import com.supvz.requests_service.model.dto.PageDto;
import com.supvz.requests_service.model.dto.RequestDto;
import com.supvz.requests_service.model.dto.RequestPayload;
import com.supvz.requests_service.model.dto.RequestUpdatePayload;
import com.supvz.requests_service.model.entity.Request;
import com.supvz.requests_service.model.entity.RequestAssignment;
import lombok.RequiredArgsConstructor;
import org.springframework.data.domain.Page;
import org.springframework.stereotype.Component;

import java.util.List;

/**
 * Реализация маппера для запросов.
 */
@Component
@RequiredArgsConstructor
public class RequestEntityMapper implements RequestMapper {
    private final RequestAssignmentMapper assignmentMapper;

    /**
     * Метод для преобразования полезной нагрузки в сущность.
     */
    @Override
    public Request create(RequestPayload payload) {
        return Request.builder()
                .pvzId(payload.pvzId())
                .appellantId(payload.appellantId())
                .subject(payload.subject())
                .description(payload.description())
                .build();
    }

    /**
     * Метод для преобразования сущности в ДТО.
     */
    @Override
    public RequestDto read(Request request) {
        List<RequestAssignment> assignments = request.getAssignments();
        return new RequestDto(
                request.getId(),
                request.getPvzId(),
                request.getAppellantId(),
                request.getSubject(),
                request.getDescription(),
                assignments == null ? List.of() : assignments.stream().map(assignmentMapper::read).toList()
        );
    }

    /**
     * Метод для преобразования Page из springframework.data.Page в ДТО
     */
    @Override
    public PageDto<RequestDto> readPage(Page<Request> page) {
        return PageDto.<RequestDto>builder()
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
    public Request update(Request request, RequestUpdatePayload payload) {
        if (payload.pvzId() != null)
            request.setPvzId(payload.pvzId());
        if (payload.subject() != null)
            request.setSubject(payload.subject());
        if (payload.description() != null)
            request.setDescription(payload.description());
        return request;
    }
}
