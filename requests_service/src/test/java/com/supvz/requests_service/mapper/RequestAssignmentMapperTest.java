package com.supvz.requests_service.mapper;

import com.supvz.requests_service.model.entity.enums.AssignmentAction;
import com.supvz.requests_service.model.dto.PageDto;
import com.supvz.requests_service.model.dto.RequestAssignmentDto;
import com.supvz.requests_service.model.dto.RequestAssignmentPayload;
import com.supvz.requests_service.model.dto.RequestAssignmentUpdatePayload;
import com.supvz.requests_service.model.entity.Request;
import com.supvz.requests_service.model.entity.RequestAssignment;
import org.junit.jupiter.api.Test;
import org.springframework.data.domain.Page;
import org.springframework.data.domain.PageImpl;

import java.time.LocalDateTime;
import java.util.List;

import static org.junit.jupiter.api.Assertions.*;
import static org.mockito.Mockito.*;

class RequestAssignmentMapperTest {
    private final RequestAssignmentEntityMapper target = new RequestAssignmentEntityMapper();

    @Test
    void create__MapsPayloadToEntity() {
        long requestIdMock = 1;
        long handymanIdMock = 1;
        String commentMock = "commentMock";
        RequestAssignmentPayload payload = new RequestAssignmentPayload(requestIdMock, handymanIdMock, commentMock);
        Request request = mock(Request.class);

        RequestAssignment result = assertDoesNotThrow(() -> target.create(request, payload));

        assertEquals(request, result.getRequest());
        assertEquals(handymanIdMock, result.getHandymanId());
        assertEquals(commentMock, result.getComment());
        assertNull(result.getId()); // ещё не сохранён
    }

    @Test
    void read__MapsEntityToDto() {
        long assignmentIdMock = 1;
        long requestIdMock = 2;
        long handymanIdMock = 1;
        AssignmentAction actionMock = mock(AssignmentAction.class);
        LocalDateTime timeMock = LocalDateTime.now();
        Request request = Request.builder().id(requestIdMock).build();
        String commentMock = "commentMock";
        RequestAssignment entityMock = RequestAssignment.builder()
                .id(assignmentIdMock)
                .request(request)
                .handymanId(handymanIdMock)
                .action(actionMock)
                .processedAt(timeMock)
                .createdAt(timeMock)
                .updatedAt(timeMock)
                .comment(commentMock)
                .build();

        RequestAssignmentDto result = assertDoesNotThrow(() -> target.read(entityMock));

        assertEquals(assignmentIdMock, result.id());
        assertEquals(requestIdMock, result.requestId());
        assertEquals(handymanIdMock, result.handymanId());
        assertEquals(actionMock, result.action());
        assertEquals(timeMock, result.processedAt());
        assertEquals(timeMock, result.createdAt());
        assertEquals(timeMock, result.updatedAt());
        assertEquals(commentMock, result.comment());
    }

    @Test
    void readPage__MapsPageOfAssignments() {
        Request requestMock = Request.builder().id(10L).build();
        long assignmentIdMock = 1;
        RequestAssignment assignmentMock = RequestAssignment.builder()
                .id(assignmentIdMock)
                .request(requestMock)
                .build();
        Page<RequestAssignment> pageMock = new PageImpl<>(List.of(assignmentMock));

        PageDto<RequestAssignmentDto> result = assertDoesNotThrow(() -> target.readPage(pageMock));

        assertEquals(0, result.page());
        assertEquals(1, result.size());
        assertEquals(1, result.total());
        assertFalse(result.hasNext());
        assertFalse(result.hasPrev());
        assertEquals(1, result.content().size());
        assertEquals(assignmentIdMock, result.content().getFirst().id());
    }

    @Test
    void update__UpdatesNonNullFields() {
        AssignmentAction oldActionMock = mock(AssignmentAction.class);
        AssignmentAction newActionMock = mock(AssignmentAction.class);
        long newHandymanMock = 2;
        String newCommentMock = "newCommentMock";
        RequestAssignment entityMock = RequestAssignment.builder()
                .id(1L)
                .handymanId(1)
                .action(oldActionMock)
                .comment("oldCommentMock")
                .build();
        RequestAssignmentUpdatePayload payloadMock = new RequestAssignmentUpdatePayload(newActionMock, newHandymanMock, newCommentMock);

        RequestAssignment result = assertDoesNotThrow(() -> target.update(entityMock, payloadMock));

        assertEquals(newHandymanMock, result.getHandymanId());
        assertEquals(newCommentMock, result.getComment());
        assertEquals(newActionMock, result.getAction());
        assertNotNull(result.getProcessedAt());
    }

    @Test
    void update__SkipsNullFields() {
        AssignmentAction actionMock = mock(AssignmentAction.class);
        String oldComment = "oldComment";
        RequestAssignment entityMock = RequestAssignment.builder()
                .handymanId(1)
                .action(actionMock)
                .comment(oldComment)
                .build();

        RequestAssignmentUpdatePayload payloadMock = new RequestAssignmentUpdatePayload(null, null, null);

        RequestAssignment updated = assertDoesNotThrow(() -> target.update(entityMock, payloadMock));

        assertEquals(entityMock.getHandymanId(), updated.getHandymanId());
        assertEquals(actionMock, updated.getAction());
        assertEquals(oldComment, updated.getComment());
    }
}