package com.supvz.requests_service.mapper.action;

import com.supvz.requests_service.core.enums.AssignmentAction;
import com.supvz.requests_service.core.enums.RequestStatus;
import com.supvz.requests_service.model.entity.Request;
import com.supvz.requests_service.model.entity.RequestAssignment;
import org.junit.jupiter.api.Test;

import java.time.LocalDateTime;

import static org.assertj.core.api.Assertions.assertThat;

class RejectActionMapperTest {

    private final RejectActionMapper target = new RejectActionMapper();

    @Test
    void map_shouldSetCorrectActionProcessedAtAndRequestStatus() {
        Request requestMock = Request.builder()
                .status(RequestStatus.pending)
                .build();
        RequestAssignment assignmentMock = RequestAssignment.builder()
                .request(requestMock)
                .handymanId(789L)
                .comment("Not available")
                .build();
        LocalDateTime beforeCall = LocalDateTime.now();


        RequestAssignment result = target.map(assignmentMock);

        assertThat(result).isSameAs(assignmentMock);
        assertThat(result.getAction()).isEqualTo(AssignmentAction.reject);
        assertThat(result.getProcessedAt()).isAfterOrEqualTo(beforeCall);
        assertThat(result.getRequest().getStatus()).isEqualTo(RequestStatus.rejected);
        assertThat(result.getHandymanId()).isEqualTo(789L);
        assertThat(result.getComment()).isEqualTo("Not available");
    }

    @Test
    void getType_shouldReturnRejectAction() {
        assertThat(target.getType()).isEqualTo(AssignmentAction.reject);
    }
}