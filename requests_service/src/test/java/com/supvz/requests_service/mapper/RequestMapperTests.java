package com.supvz.requests_service.mapper;

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
class RequestMapperTests {
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
        Request requestMock = Request.builder()
                .id(requestIdMock)
                .pvzId(pvzIdMock)
                .appellantId(appellantIdMock)
                .description(descriptionMock)
                .subject(subjectMock)
                .assignments(List.of(assignmentMock))
                .build();

        when(assignmentMapper.read(assignmentMock)).thenReturn(assignmentDtoMock);

        RequestDto result = assertDoesNotThrow(() -> target.read(requestMock));

        assertEquals(requestIdMock, result.id());
        assertEquals(pvzIdMock, result.pvzId());
        assertEquals(appellantIdMock, result.appellantId());
        assertEquals(subjectMock, result.subject());
        assertEquals(descriptionMock, result.description());
        assertEquals(1, result.assignments().size());
    }

    @Test
    void read__HandlesNullAssignments() {
        Request requestMock = Request.builder()
                .id(1L)
                .pvzId(123)
                .description("desc")
                .assignments(null)
                .build();


        RequestDto result = assertDoesNotThrow(() -> target.read(requestMock));

        assertTrue(result.assignments().isEmpty());
    }

    @Test
    void readPage__MapsPageOfRequests() {
        Request requestMock = Request.builder()
                .id(1L)
                .pvzId(123)
                .description("desc")
                .assignments(List.of())
                .build();

        Page<Request> page = new PageImpl<>(List.of(requestMock));

        PageDto<RequestPlainDto> result = assertDoesNotThrow(() -> target.readPage(page));

        assertEquals(0, result.page());
        assertEquals(1, result.size());
        assertEquals(1, result.total());
        assertFalse(result.hasNext());
        assertFalse(result.hasPrev());
        assertTrue(result.content().stream().map(RequestPlainDto::id).toList().contains(1L));
    }

    @Test
    void update__UpdatesNonNullFields() {
        Request requestMock = Request.builder()
                .id(1L)
                .pvzId(100)
                .subject("oldSubject")
                .description("oldDescription")
                .build();

        int newPvzIdMock = 200;
        String newSubjectMock = "newSubjectMock";
        String newDescriptionMock = "newDescriptionMock";
        RequestUpdatePayload payloadMock = new RequestUpdatePayload(newPvzIdMock, newSubjectMock, newDescriptionMock);

        Request updated = assertDoesNotThrow(() -> target.update(requestMock, payloadMock));

        assertEquals(newPvzIdMock, updated.getPvzId());
        assertEquals(newSubjectMock, updated.getSubject());
        assertEquals(newDescriptionMock, updated.getDescription());
    }

    @Test
    void update__SkipsNullFields() {
        int oldPvzIdMock = 100;
        String oldDescriptionMock = "oldDescriptionMock";
        String oldSubjectMock = "oldSubjectMock";
        Request requestMock = Request.builder()
                .pvzId(oldPvzIdMock)
                .description(oldDescriptionMock)
                .subject(oldSubjectMock)
                .build();
        RequestUpdatePayload payloadMock = new RequestUpdatePayload(null, null, null);

        Request result = assertDoesNotThrow(() -> target.update(requestMock, payloadMock));

        assertEquals(oldPvzIdMock, result.getPvzId());
        assertEquals(oldSubjectMock, result.getSubject());
        assertEquals(oldDescriptionMock, result.getDescription());
    }
}