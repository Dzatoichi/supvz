package com.supvz.requests_service.core.filter;

import com.supvz.requests_service.core.enums.AssignmentAction;

public record RequestAssignmentFilter(
        Long requestId,
        Long handymanId,
        AssignmentAction action
) {
}
