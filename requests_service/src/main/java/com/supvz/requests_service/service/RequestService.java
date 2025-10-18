package com.supvz.requests_service.service;

import com.supvz.requests_service.core.*;
import com.supvz.requests_service.entity.Request;

/*
Интерфейс сервиса для работы с запросами.
 */
public interface RequestService {
    RequestDto create(RequestPayload payload);

    PageDto<RequestDto> readAll(int page, int size, RequestFilter filter);

    RequestDto read(long id);

    RequestDto update(long id, RequestUpdatePayload payload);

    void delete(long id);

    Request get(long id);
}
