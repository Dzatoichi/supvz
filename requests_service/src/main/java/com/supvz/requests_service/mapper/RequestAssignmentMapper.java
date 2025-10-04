package com.supvz.requests_service.mapper;

import com.supvz.requests_service.core.PageDto;
import com.supvz.requests_service.core.RequestAssignmentDto;
import com.supvz.requests_service.core.RequestAssignmentPayload;
import com.supvz.requests_service.core.RequestAssignmentUpdatePayload;
import com.supvz.requests_service.entity.Request;
import com.supvz.requests_service.entity.RequestAssignment;
import org.springframework.data.domain.Page;

public interface RequestAssignmentMapper {
    RequestAssignment create(Request request, RequestAssignmentPayload payload);

    RequestAssignmentDto read(RequestAssignment requestAssignment);

    PageDto<RequestAssignmentDto> readPage(Page<RequestAssignment> page);

    RequestAssignment update(RequestAssignment found, RequestAssignmentUpdatePayload payload);
}
