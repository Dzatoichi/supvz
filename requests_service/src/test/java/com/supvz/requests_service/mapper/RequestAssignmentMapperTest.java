package com.supvz.requests_service.mapper;

import com.supvz.requests_service.core.*;
import com.supvz.requests_service.entity.Request;
import com.supvz.requests_service.entity.RequestAssignment;
import com.supvz.requests_service.mapper.impl.RequestAssignmentMapperImpl;
import org.junit.jupiter.api.Test;
import org.junit.jupiter.api.extension.ExtendWith;
import org.mockito.InjectMocks;
import org.mockito.junit.jupiter.MockitoExtension;
import org.springframework.data.domain.Page;
import org.springframework.data.domain.PageImpl;

import java.time.LocalDateTime;
import java.util.List;
import java.util.UUID;

import static org.junit.jupiter.api.Assertions.*;

@ExtendWith(MockitoExtension.class)
class RequestAssignmentMapperTest {
    @InjectMocks
    private RequestAssignmentMapperImpl mapper;

    @Test
    void read__MapsEntityToDto() {
        Request request = Request.builder().id(10L).build();
        UUID handymanId = UUID.randomUUID();
        LocalDateTime now = LocalDateTime.now();

        RequestAssignment assignment = RequestAssignment.builder()
                .id(1L)
                .request(request)
                .handymanId(handymanId)
                .status(Status.ASSIGNED)
                .assignedAt(now)
                .completedAt(null)
                .description("fix sink")
                .build();

        var dto = mapper.read(assignment);

        assertEquals(1L, dto.id());
        assertEquals(10L, dto.requestId());
        assertEquals(handymanId, dto.handymanId());
        assertEquals(Status.ASSIGNED, dto.status());
        assertEquals(now, dto.assignedAt());
        assertNull(dto.completedAt());
        assertEquals("fix sink", dto.description());
    }

    @Test
    void create__MapsPayloadToEntity() {
        Request request = Request.builder().id(10L).build();
        UUID handymanId = UUID.randomUUID();

        RequestAssignmentPayload payload = new RequestAssignmentPayload(handymanId, "test job");

        RequestAssignment assignment = mapper.create(request, payload);

        assertEquals(request, assignment.getRequest());
        assertEquals(handymanId, assignment.getHandymanId());
        assertEquals("test job", assignment.getDescription());
        assertNull(assignment.getId()); // ещё не сохранён
    }

    @Test
    void readPage__MapsPageOfAssignments() {
        Request request = Request.builder().id(10L).build();
        RequestAssignment assignment = RequestAssignment.builder()
                .id(1L)
                .request(request)
                .handymanId(UUID.randomUUID())
                .status(Status.ASSIGNED)
                .description("job")
                .build();

        Page<RequestAssignment> page = new PageImpl<>(List.of(assignment));

        var dtoPage = mapper.readPage(page);

        assertEquals(0, dtoPage.page());
        assertEquals(1, dtoPage.size());
        assertEquals(1, dtoPage.total());
        assertFalse(dtoPage.hasNext());
        assertFalse(dtoPage.hasPrev());
        assertEquals(1, dtoPage.content().size());
        assertEquals(1L, dtoPage.content().getFirst().id());
    }

    @Test
    void update__UpdatesNonNullFieldsAndSetsCompletedAt_WhenConfirmed() {
        RequestAssignment assignment = RequestAssignment.builder()
                .id(1L)
                .handymanId(UUID.randomUUID())
                .status(Status.ASSIGNED)
                .description("old job")
                .build();

        UUID newHandyman = UUID.randomUUID();
        RequestAssignmentUpdatePayload payload = new RequestAssignmentUpdatePayload(Status.CONFIRMED, newHandyman, "updated");

        RequestAssignment updated = mapper.update(assignment, payload);

        assertEquals(newHandyman, updated.getHandymanId());
        assertEquals(Status.CONFIRMED, updated.getStatus());
        assertNotNull(updated.getCompletedAt());
        assertEquals("updated", updated.getDescription());
    }

    @Test
    void update__SetsCompletedAt_WhenRejected() {
        RequestAssignment assignment = RequestAssignment.builder()
                .status(Status.ASSIGNED)
                .description("old job")
                .build();

        RequestAssignmentUpdatePayload payload = new RequestAssignmentUpdatePayload(Status.REJECTED, null, null);

        RequestAssignment updated = mapper.update(assignment, payload);

        assertEquals(Status.REJECTED, updated.getStatus());
        assertNotNull(updated.getCompletedAt());
    }

    @Test
    void update__SkipsNullFields() {
        RequestAssignment assignment = RequestAssignment.builder()
                .handymanId(UUID.randomUUID())
                .status(Status.ASSIGNED)
                .description("old job")
                .build();

        RequestAssignmentUpdatePayload payload = new RequestAssignmentUpdatePayload(null, null, null);

        RequestAssignment updated = mapper.update(assignment, payload);

        assertEquals(assignment.getHandymanId(), updated.getHandymanId());
        assertEquals(Status.ASSIGNED, updated.getStatus());
        assertEquals("old job", updated.getDescription());
        assertNull(updated.getCompletedAt());
    }

}