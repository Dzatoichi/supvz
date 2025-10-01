package com.supvz.requests_service.mapper;

import com.supvz.requests_service.core.PageDto;
import com.supvz.requests_service.core.RequestDto;
import com.supvz.requests_service.core.RequestPayload;
import com.supvz.requests_service.core.RequestUpdatePayload;
import com.supvz.requests_service.entity.Request;
import org.springframework.data.domain.Page;

public interface RequestMapper {
    Request create(RequestPayload payload);

    RequestDto read(Request request);

    PageDto<RequestDto> readPage(Page<Request> page);

    Request update(Request found, RequestUpdatePayload payload);
}
