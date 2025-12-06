package com.supvz.requests_service.mapper;

import com.supvz.requests_service.core.enums.AssignmentAction;
import com.supvz.requests_service.core.enums.RequestStatus;
import com.supvz.requests_service.model.entity.RequestAssignment;
import lombok.RequiredArgsConstructor;
import org.springframework.stereotype.Component;
import org.springframework.transaction.annotation.Transactional;

import java.time.LocalDateTime;

@Component
@RequiredArgsConstructor
public class CancelActionMapper implements ActionMapper {

    @Override
    @Transactional
    public RequestAssignment map(RequestAssignment assignment) {
        assignment.setProcessedAt(LocalDateTime.now());
        assignment.setAction(this.getType());
        assignment.getRequest().setStatus(RequestStatus.pending);
        return assignment;
    }

    /**
     * Метод для реализации паттерна Strategy
     * @return {@link AssignmentAction} - тип, с которым работает данный процессор.
     */
    @Override
    public AssignmentAction getType() {
        return AssignmentAction.cancel;
    }
}
