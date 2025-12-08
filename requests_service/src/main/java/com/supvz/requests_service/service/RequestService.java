package com.supvz.requests_service.service;

import com.supvz.requests_service.core.enums.RequestStatus;
import com.supvz.requests_service.core.filter.RequestFilter;
import com.supvz.requests_service.model.dto.*;
import com.supvz.requests_service.model.entity.Request;

/*
Интерфейс сервиса для работы с запросами.
 */
public interface RequestService {
    RequestDto create(RequestPayload payload);

    PageDto<RequestPlainDto> readAll(int page, int size, RequestFilter filter);

    RequestDto read(long id);

    RequestDto update(long id, RequestUpdatePayload payload);

    void delete(long id);

    Request get(long id);

    Request assign(long request);

    void setStatus(Request request, RequestStatus requestStatus);
}
