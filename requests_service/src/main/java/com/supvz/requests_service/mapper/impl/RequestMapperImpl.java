package com.supvz.requests_service.mapper.impl;

import com.supvz.requests_service.core.*;
import com.supvz.requests_service.entity.Request;
import com.supvz.requests_service.entity.RequestAssignment;
import com.supvz.requests_service.mapper.RequestAssignmentMapper;
import com.supvz.requests_service.mapper.RequestMapper;
import lombok.RequiredArgsConstructor;
import org.springframework.data.domain.Page;
import org.springframework.stereotype.Component;

import java.util.List;

@Component
@RequiredArgsConstructor
/*
Реализация маппера для запросов.
 */
public class RequestMapperImpl implements RequestMapper {
    private final RequestAssignmentMapper assignmentMapper;

    @Override
    /*
    Метод для преобразования полезной нагрузки в сущность.
     */
    public Request create(RequestPayload payload) {
        return Request.builder()
                .pvzId(payload.pvzId())
                .appellantId(payload.appellantId())
                .description(payload.description())
                .build();
    }

    @Override
    /*
    Метод для преобразования сущности в ДТО.
     */
    public RequestDto read(Request request) {
        List<RequestAssignment> assignments = request.getAssignments();

        return RequestDto.builder()
                .id(request.getId())
                .appellantId(request.getAppellantId())
                .pvzId(request.getPvzId())
                .description(request.getDescription())
                .assignments(assignments == null ? List.of() : assignments.stream().map(assignmentMapper::read).toList())
                .build();
    }

    @Override
    /*
    Метод для преобразования Page из springframework.data.Page в ДТО
     */
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

    @Override
    /*
    Метод для преобразования сущности и полезной нагрузки для обновления в сущность.
     */
    public Request update(Request request, RequestUpdatePayload payload) {
        String description = payload.description();
        Integer pvzId = payload.pvzId();

        if (pvzId != null)
            request.setPvzId(pvzId);
        if (description != null)
            request.setDescription(description);

        return request;
    }
}
