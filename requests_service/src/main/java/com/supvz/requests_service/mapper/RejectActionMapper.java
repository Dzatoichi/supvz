package com.supvz.requests_service.mapper;

import com.supvz.requests_service.core.enums.AssignmentAction;
import com.supvz.requests_service.core.enums.RequestStatus;
import com.supvz.requests_service.model.entity.RequestAssignment;
import org.springframework.stereotype.Component;

import java.time.LocalDateTime;

@Component
public class RejectActionMapper implements ActionMapper {
    @Override
    public RequestAssignment map(RequestAssignment assignment) {
        assignment.setProcessedAt(LocalDateTime.now());
        assignment.setAction(this.getType());
        assignment.getRequest().setStatus(RequestStatus.rejected);
        return assignment;
    }

    @Override
    public AssignmentAction getType() {
        return AssignmentAction.reject;
    }
}
