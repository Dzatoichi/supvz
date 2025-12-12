package com.supvz.requests_service.mapper.action;

import com.supvz.requests_service.core.enums.AssignmentAction;
import com.supvz.requests_service.core.enums.RequestStatus;
import com.supvz.requests_service.model.entity.Request;
import com.supvz.requests_service.model.entity.RequestAssignment;
import org.junit.jupiter.api.Test;

import java.time.LocalDateTime;

import static org.assertj.core.api.Assertions.assertThat;
import static org.junit.jupiter.api.Assertions.assertDoesNotThrow;

class CompleteActionMapperTests {

    private final CompleteActionMapper target = new CompleteActionMapper();

    @Test
    void map_shouldSetCorrectActionProcessedAtAndRequestStatus() {
        Request requestMock = Request.builder()
                .status(RequestStatus.assigned)
                .build();
        RequestAssignment assignmentMock = RequestAssignment.builder()
                .request(requestMock)
                .handymanId(456L)
                .comment("Work done")
                .build();

        LocalDateTime beforeCall = LocalDateTime.now();

        RequestAssignment result = assertDoesNotThrow(() -> target.map(assignmentMock));

        assertThat(result).isSameAs(assignmentMock);
        assertThat(result.getAction()).isEqualTo(AssignmentAction.complete);
        assertThat(result.getProcessedAt()).isAfterOrEqualTo(beforeCall);
        assertThat(result.getRequest().getStatus()).isEqualTo(RequestStatus.completed);
        assertThat(result.getHandymanId()).isEqualTo(456L);
        assertThat(result.getComment()).isEqualTo("Work done");
    }

    @Test
    void getType_shouldReturnCompleteAction() {
        assertThat(target.getType()).isEqualTo(AssignmentAction.complete);
    }
}