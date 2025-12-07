package com.supvz.requests_service.mapper.entity;

import com.supvz.requests_service.model.dto.*;
import com.supvz.requests_service.model.entity.Request;
import com.supvz.requests_service.model.entity.RequestAssignment;
import org.junit.jupiter.api.Test;
import org.junit.jupiter.api.extension.ExtendWith;
import org.mockito.InjectMocks;
import org.mockito.Mock;
import org.mockito.junit.jupiter.MockitoExtension;
import org.springframework.data.domain.Page;
import org.springframework.data.domain.PageImpl;

import java.util.List;

import static org.junit.jupiter.api.Assertions.*;
import static org.mockito.Mockito.mock;
import static org.mockito.Mockito.when;

@ExtendWith(MockitoExtension.class)
class RequestMapperTest {
    @InjectMocks
    private RequestEntityMapper target;
    @Mock
    private RequestAssignmentMapper assignmentMapper;

    @Test
    void create__MapsPayloadToEntity() {
        int pvzIdMock = 12;
        long appellantIdMock = 1;
        String subjectMock = "subjectMock";
        String descriptionMock = "descriptionMock";
        RequestPayload payload = new RequestPayload(pvzIdMock, appellantIdMock, subjectMock, descriptionMock);

        Request result = assertDoesNotThrow(() -> target.create(payload));

        assertEquals(pvzIdMock, result.getPvzId());
        assertEquals(appellantIdMock, result.getAppellantId());
        assertEquals(subjectMock, result.getSubject());
        assertEquals(descriptionMock, result.getDescription());
        assertNull(result.getAssignments());
    }

    @Test
    void read__MapsEntityToDto_WithAssignments() {
        RequestAssignment assignmentMock = mock(RequestAssignment.class);
        RequestAssignmentDto assignmentDtoMock = mock(RequestAssignmentDto.class);
        long requestIdMock = 1L;
        int pvzIdMock = 123;
        long appellantIdMock = 12;
        String descriptionMock = "descriptionMock";
        String subjectMock = "subjectMock";
        Request request = Request.builder()
                .id(requestIdMock)
                .pvzId(pvzIdMock)
                .appellantId(appellantIdMock)
                .description(descriptionMock)
                .subject(subjectMock)
                .assignments(List.of(assignmentMock))
                .build();

        when(assignmentMapper.read(assignmentMock)).thenReturn(assignmentDtoMock);

        RequestDto result = assertDoesNotThrow(() -> target.read(request));

        assertEquals(requestIdMock, result.id());
        assertEquals(pvzIdMock, result.pvzId());
        assertEquals(appellantIdMock, result.appellantId());
        assertEquals(subjectMock, result.subject());
        assertEquals(descriptionMock, result.description());
        assertEquals(1, result.assignments().size());
    }

    @Test
    void read__HandlesNullAssignments() {
        Request request = Request.builder()
                .id(1L)
                .pvzId(123)
                .description("desc")
                .assignments(null)
                .build();

        RequestDto dto = target.read(request);

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

        PageDto<RequestDto> dtoPage = target.readPage(page);

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
                .subject("oldSubject")
                .description("oldDescription")
                .build();

        int newPvzId = 200;
        String newSubject = "newSubject";
        String newDescription = "newDescription";
        RequestUpdatePayload payload = new RequestUpdatePayload(newPvzId, newSubject, newDescription);

        Request updated = target.update(request, payload);

        assertEquals(newPvzId, updated.getPvzId());
        assertEquals(newSubject, updated.getSubject());
        assertEquals(newDescription, updated.getDescription());
    }

    @Test
    void update__SkipsNullFields() {
        int oldPvzId = 100;
        String oldDescription = "oldDescription";
        String oldSubject = "oldSubject";
        Request request = Request.builder()
                .pvzId(oldPvzId)
                .description(oldDescription)
                .subject(oldSubject)
                .build();

        RequestUpdatePayload payload = new RequestUpdatePayload(null, null, null);

        Request updated = target.update(request, payload);

        assertEquals(oldPvzId, updated.getPvzId());
        assertEquals(oldSubject, updated.getSubject());
        assertEquals(oldDescription, updated.getDescription());
    }
}