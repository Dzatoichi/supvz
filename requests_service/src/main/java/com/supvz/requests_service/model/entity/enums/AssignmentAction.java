package com.supvz.requests_service.model.entity.enums;

import lombok.Getter;

@Getter
public enum AssignmentAction {
    assign(RequestStatus.assigned),
    self_cancel(RequestStatus.pending),
    system_cancel,
    reject(RequestStatus.rejected),
    complete(RequestStatus.completed);

    private final RequestStatus targetRequestStatus;

    AssignmentAction() {
        this.targetRequestStatus = null;
    }
    AssignmentAction(RequestStatus requestStatus) {
        this.targetRequestStatus = requestStatus;
    }
}