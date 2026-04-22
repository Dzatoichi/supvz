package com.supvz.requests_service.service;

import com.supvz.requests_service.core.filter.RequestAssignmentFilter;
import com.supvz.requests_service.model.dto.PageDto;
import com.supvz.requests_service.model.dto.RequestAssignmentDto;
import com.supvz.requests_service.model.dto.RequestAssignmentPayload;
import com.supvz.requests_service.model.dto.RequestAssignmentUpdatePayload;

/*
Интерфейс сервиса для работы с ответами на запросы.
 */
public interface RequestAssignmentService {
    RequestAssignmentDto create(RequestAssignmentPayload payload);

    PageDto<RequestAssignmentDto> readAll(int page, int size, RequestAssignmentFilter filter);

    RequestAssignmentDto read(long id);

    RequestAssignmentDto update(long id, RequestAssignmentUpdatePayload payload);
}