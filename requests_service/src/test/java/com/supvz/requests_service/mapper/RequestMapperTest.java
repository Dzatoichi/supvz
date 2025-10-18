package com.supvz.requests_service.mapper;

import com.supvz.requests_service.core.*;
import com.supvz.requests_service.entity.Request;
import com.supvz.requests_service.entity.RequestAssignment;
import com.supvz.requests_service.mapper.impl.RequestMapperImpl;
import org.junit.jupiter.api.Test;
import org.junit.jupiter.api.extension.ExtendWith;
import org.mockito.InjectMocks;
import org.mockito.Mock;
import org.mockito.junit.jupiter.MockitoExtension;
import org.springframework.data.domain.Page;
import org.springframework.data.domain.PageImpl;

import java.util.List;
import java.util.UUID;

import static org.junit.jupiter.api.Assertions.*;
import static org.mockito.Mockito.when;

@ExtendWith(MockitoExtension.class)
class RequestMapperTest {
    @InjectMocks
    private RequestMapperImpl mapper;

    @Mock
    private RequestAssignmentMapper assignmentMapper;

    @Test
    void create__MapsPayloadToEntity() {
        UUID userId = UUID.randomUUID();
        RequestPayload payload = new RequestPayload(123, userId, "desc");

        Request request = mapper.create(payload);

        assertEquals(123, request.getPvzId());
        assertEquals(userId, request.getAppellantId());
        assertEquals("desc", request.getDescription());
        assertNull(request.getAssignments());
    }

    @Test
    void read__MapsEntityToDto_WithAssignments() {
        UUID userId = UUID.randomUUID();
        RequestAssignment assignment = new RequestAssignment();
        Request request = Request.builder()
                .id(1L)
                .pvzId(123)
                .appellantId(userId)
                .description("desc")
                .assignments(List.of(assignment))
                .build();

        when(assignmentMapper.read(assignment))
                .thenReturn(RequestAssignmentDto.builder()
                        .id(2L)
                        .description("child")
                        .build());


        RequestDto dto = mapper.read(request);

        assertEquals(1L, dto.id());
        assertEquals(123, dto.pvzId());
        assertEquals(userId, dto.appellantId());
        assertEquals("desc", dto.description());
        assertEquals(1, dto.assignments().size());
    }

    @Test
    void read__HandlesNullAssignments() {
        Request request = Request.builder()
                .id(1L)
                .pvzId(123)
                .description("desc")
                .assignments(null)
                .build();

        RequestDto dto = mapper.read(request);

        assertTrue(dto.assignments().isEmpty());
    }

    @Test
    void readPage__MapsPageOfRequests() {
        Request request = Request.builder()
                .id(1L)
                .pvzId(123)
                .description("desc")
                .assignments(List.of())
                .build();

        Page<Request> page = new PageImpl<>(List.of(request));

        PageDto<RequestDto> dtoPage = mapper.readPage(page);

        assertEquals(0, dtoPage.page());
        assertEquals(1, dtoPage.size());
        assertEquals(1, dtoPage.total());
        assertFalse(dtoPage.hasNext());
        assertFalse(dtoPage.hasPrev());
        assertTrue(dtoPage.content().stream().map(RequestDto::id).toList().contains(1L));
    }

    @Test
    void update__UpdatesNonNullFields() {
        Request request = Request.builder()
                .id(1L)
                .pvzId(100)
                .description("old")
                .build();

        RequestUpdatePayload payload = new RequestUpdatePayload(200, "new");

        Request updated = mapper.update(request, payload);

        assertEquals(200, updated.getPvzId());
        assertEquals("new", updated.getDescription());
    }

    @Test
    void update__SkipsNullFields() {
        Request request = Request.builder()
                .pvzId(100)
                .description("old")
                .build();

        RequestUpdatePayload payload = new RequestUpdatePayload(null, null);

        Request updated = mapper.update(request, payload);

        assertEquals(100, updated.getPvzId());
        assertEquals("old", updated.getDescription());
    }
}