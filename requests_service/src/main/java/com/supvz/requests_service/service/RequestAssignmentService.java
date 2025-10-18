package com.supvz.requests_service.service;

import com.supvz.requests_service.core.PageDto;
import com.supvz.requests_service.core.RequestAssignmentDto;
import com.supvz.requests_service.core.RequestAssignmentPayload;
import com.supvz.requests_service.core.RequestAssignmentUpdatePayload;

/*
Интерфейс сервиса для работы с ответами на запросы.
 */
public interface RequestAssignmentService {
    RequestAssignmentDto create(long id, RequestAssignmentPayload payload);

    PageDto<RequestAssignmentDto> readAll(long requestId, int page, int size);

    RequestAssignmentDto read(long id);

    RequestAssignmentDto update(long id, RequestAssignmentUpdatePayload payload);

    void delete(long id);
}
