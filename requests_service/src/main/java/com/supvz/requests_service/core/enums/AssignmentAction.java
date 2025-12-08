package com.supvz.requests_service.core.enums;

import lombok.Getter;

@Getter
public enum AssignmentAction {
    assign(RequestStatus.assigned),
    cancel(RequestStatus.pending),
    reject(RequestStatus.rejected),
    complete(RequestStatus.completed);

    private final RequestStatus targetRequestStatus;

    AssignmentAction(RequestStatus requestStatus) {
        this.targetRequestStatus = requestStatus;
    }
}