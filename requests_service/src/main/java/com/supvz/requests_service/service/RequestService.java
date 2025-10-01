package com.supvz.requests_service.service;

import com.supvz.requests_service.core.*;
import com.supvz.requests_service.entity.Request;
import jakarta.validation.Valid;

public interface RequestService {
    RequestDto create(RequestPayload payload);

    PageDto<RequestDto> readAll(int page, int size, RequestFilter filter);

    RequestDto read(long id);

    void delete(long id);

    Request get(long id);

    RequestDto update(long id, RequestUpdatePayload payload);
}
