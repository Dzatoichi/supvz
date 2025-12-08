package com.supvz.requests_service.mapper.action;

import com.supvz.requests_service.core.enums.AssignmentAction;
import com.supvz.requests_service.core.enums.RequestStatus;
import com.supvz.requests_service.model.entity.Request;
import com.supvz.requests_service.model.entity.RequestAssignment;
import org.junit.jupiter.api.Test;

import java.time.LocalDateTime;

import static org.assertj.core.api.Assertions.assertThat;
import static org.junit.jupiter.api.Assertions.assertDoesNotThrow;
import static org.mockito.Mockito.mock;

class CancelActionMapperTests {

    private final CancelActionMapper target = new CancelActionMapper();

    @Test
    void map_shouldUpdateRequestAssignmentForCancelAction() {
        RequestStatus statusMock = mock(RequestStatus.class);
        Request requestMock = Request.builder().status(statusMock).build();

        RequestAssignment assignmentMock = RequestAssignment.builder()
                .request(requestMock)
                .handymanId(123L)
                .comment("Initial comment")
                .build();

        LocalDateTime beforeCall = LocalDateTime.now();

        RequestAssignment result = assertDoesNotThrow(() -> target.map(assignmentMock));

        assertThat(result).isSameAs(assignmentMock);
        assertThat(result.getAction()).isEqualTo(AssignmentAction.cancel);
        assertThat(result.getRequest().getStatus()).isEqualTo(RequestStatus.pending);
        assertThat(result.getProcessedAt()).isAfterOrEqualTo(beforeCall);
        assertThat(result.getComment()).isEqualTo("Initial comment");
        assertThat(result.getHandymanId()).isEqualTo(123L);
    }

    @Test
    void getType_shouldReturnCancelAction() {
        AssignmentAction type = target.getType();
        assertThat(type).isEqualTo(AssignmentAction.cancel);
    }
}