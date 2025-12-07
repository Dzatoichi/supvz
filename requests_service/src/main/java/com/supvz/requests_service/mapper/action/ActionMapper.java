package com.supvz.requests_service.mapper.action;

import com.supvz.requests_service.core.enums.AssignmentAction;
import com.supvz.requests_service.model.entity.RequestAssignment;

public interface ActionMapper {
    RequestAssignment map(RequestAssignment assignment);
    AssignmentAction getType();
}
