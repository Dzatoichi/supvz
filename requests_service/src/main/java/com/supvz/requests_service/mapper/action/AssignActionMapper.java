package com.supvz.requests_service.mapper.action;

import com.supvz.requests_service.core.enums.AssignmentAction;
import com.supvz.requests_service.core.enums.RequestStatus;
import com.supvz.requests_service.model.entity.Request;
import com.supvz.requests_service.model.entity.RequestAssignment;
import com.supvz.requests_service.service.RequestService;
import lombok.RequiredArgsConstructor;
import lombok.extern.slf4j.Slf4j;
import org.springframework.stereotype.Component;

import java.time.LocalDateTime;

@Slf4j
@Component
@RequiredArgsConstructor
public class AssignActionMapper implements ActionMapper{
    private final RequestService requestService;
    @Override
    public RequestAssignment map(RequestAssignment assignment) {
        requestService.setStatus(assignment.getRequest(), RequestStatus.pending);
        assignment.setProcessedAt(LocalDateTime.now());
        assignment.setAction(this.getType());
        return assignment;
    }

    @Override
    public AssignmentAction getType() {
        return AssignmentAction.assign;
    }
}
// todo: написать тесты и комментарии.