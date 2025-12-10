package com.supvz.requests_service.service;

import com.supvz.requests_service.core.exception.RequestAssignmentNotFoundException;
import com.supvz.requests_service.core.exception.RequestNotFoundException;
import com.supvz.requests_service.core.filter.RequestAssignmentFilter;
import com.supvz.requests_service.model.dto.PageDto;
import com.supvz.requests_service.model.dto.RequestAssignmentDto;
import com.supvz.requests_service.model.dto.RequestAssignmentPayload;
import com.supvz.requests_service.model.dto.RequestAssignmentUpdatePayload;
import com.supvz.requests_service.model.entity.Request;
import com.supvz.requests_service.model.entity.RequestAssignment;
import com.supvz.requests_service.mapper.entity.RequestAssignmentMapper;
import com.supvz.requests_service.repo.RequestAssignmentRepository;
import org.junit.jupiter.api.Assertions;
import org.junit.jupiter.api.Test;
import org.junit.jupiter.api.extension.ExtendWith;
import org.mockito.InjectMocks;
import org.mockito.Mock;
import org.mockito.junit.jupiter.MockitoExtension;
import org.springframework.data.domain.Page;
import org.springframework.data.domain.Pageable;
import org.springframework.data.jpa.domain.Specification;

import java.util.Optional;

import static org.junit.jupiter.api.Assertions.*;
import static org.mockito.Mockito.*;

@ExtendWith(MockitoExtension.class)
class RequestAssignmentServiceTests {
    @InjectMocks
    private RequestAssignmentEntityService target;
    @Mock
    private RequestAssignmentMapper mapper;
    @Mock
    private RequestAssignmentRepository repo;
    @Mock
    private RequestService requestService;


    @Test
    void create__ReturnsRequestAssignmentDto() {
        long requestIdMock = 1;
        RequestAssignmentPayload payloadMock = new RequestAssignmentPayload(requestIdMock, 1, null);
        Request entityMock = mock(Request.class);
        RequestAssignment mappedMock = mock(RequestAssignment.class);
        RequestAssignment savedMock = mock(RequestAssignment.class);
        RequestAssignmentDto dtoMock = mock(RequestAssignmentDto.class);

        when(requestService.get(requestIdMock)).thenReturn(entityMock);
        when(mapper.create(entityMock, payloadMock)).thenReturn(mappedMock);
        when(repo.save(mappedMock)).thenReturn(savedMock);
        when(mapper.read(savedMock)).thenReturn(dtoMock);

        RequestAssignmentDto result = assertDoesNotThrow(() -> target.create(payloadMock));
        assertEquals(dtoMock, result);

        verify(requestService, times(1)).get(requestIdMock);
        verify(mapper, times(1)).create(entityMock, payloadMock);
        verify(repo, times(1)).save(mappedMock);
        verify(mapper, times(1)).read(savedMock);
    }

    @Test
    void create__RequestNotFound__ThrowsException() {
        long requestIdMock = 1;
        RequestAssignmentPayload payloadMock = new RequestAssignmentPayload(requestIdMock, 1, null);

        when(requestService.get(requestIdMock)).thenThrow(RequestNotFoundException.class);
        assertThrows(RequestNotFoundException.class, () -> target.create(payloadMock));

        verify(requestService, times(1)).get(requestIdMock);
        verifyNoInteractions(mapper, repo);
    }

    @Test
    void readAll__ReturnsPageDto() {
        RequestAssignmentFilter filterMock = mock(RequestAssignmentFilter.class);
        Page<RequestAssignment> pageMock = mock(Page.class);
        PageDto<RequestAssignmentDto> dtoMock = mock(PageDto.class);

        when(repo.findAll(any(Specification.class), any(Pageable.class))).thenReturn(pageMock);
        when(mapper.readPage(pageMock)).thenReturn(dtoMock);

        PageDto<RequestAssignmentDto> result = assertDoesNotThrow(() -> target.readAll(1, 1, filterMock));
        assertEquals(dtoMock, result);

        verify(repo, times(1)).findAll(any(Specification.class), any(Pageable.class));
        verify(mapper, times(1)).readPage(pageMock);
    }

    @Test
    void read__ReturnsRequestAssignmentDto() {
        long assignmentIdMock = 1;
        RequestAssignment entityMock = mock(RequestAssignment.class);
        RequestAssignmentDto dtoMock = mock(RequestAssignmentDto.class);

        when(repo.findById(assignmentIdMock)).thenReturn(Optional.of(entityMock));
        when(mapper.read(entityMock)).thenReturn(dtoMock);

        RequestAssignmentDto result = Assertions.assertDoesNotThrow(() -> target.read(assignmentIdMock));
        Assertions.assertEquals(dtoMock, result);

        verify(repo, times(1)).findById(assignmentIdMock);
        verify(mapper, times(1)).read(entityMock);
    }

    @Test
    void read__RequestAssignmentNotFound__ThrowsException() {
        long assignmentIdMock = 1;

        when(repo.findById(assignmentIdMock)).thenReturn(Optional.empty());
        Assertions.assertThrows(RequestAssignmentNotFoundException.class, () -> target.read(assignmentIdMock));

        verify(repo, times(1)).findById(assignmentIdMock);
        verifyNoInteractions(mapper);
    }


    @Test
    void update__ReturnsRequestDto() {
        long assignmentIdMock = 1;
        RequestAssignmentUpdatePayload payloadMock = mock(RequestAssignmentUpdatePayload.class);
        RequestAssignment entityMock = mock(RequestAssignment.class);
        RequestAssignmentDto dtoMock = mock(RequestAssignmentDto.class);

        when(repo.findById(assignmentIdMock)).thenReturn(Optional.of(entityMock));
        when(mapper.update(entityMock, payloadMock)).thenReturn(entityMock);
        when(repo.save(entityMock)).thenReturn(entityMock);
        when(mapper.read(entityMock)).thenReturn(dtoMock);

        RequestAssignmentDto result = Assertions.assertDoesNotThrow(() -> target.update(assignmentIdMock, payloadMock));
        Assertions.assertEquals(dtoMock, result);

        verify(repo, times(1)).findById(assignmentIdMock);
        verify(mapper, times(1)).update(entityMock, payloadMock);
        verify(repo, times(1)).save(entityMock);
        verify(mapper, times(1)).read(entityMock);
    }


    @Test
    void update__RequestAssignmentNotFound__ThrowsException() {
        long assignmentIdMock = 1;
        RequestAssignmentUpdatePayload payloadMock = mock(RequestAssignmentUpdatePayload.class);

        when(repo.findById(assignmentIdMock)).thenReturn(Optional.empty());

        Assertions.assertThrows(RequestAssignmentNotFoundException.class, () -> target.update(assignmentIdMock, payloadMock));

        verify(repo, times(1)).findById(assignmentIdMock);
        verifyNoInteractions(mapper);
        verifyNoMoreInteractions(repo);
    }

    @Test
    void delete__DoesNotThrowsException() {
        long assignmentIdMock = 1;
        RequestAssignment entityMock = mock(RequestAssignment.class);

        when(repo.findById(assignmentIdMock)).thenReturn(Optional.of(entityMock));

        Assertions.assertDoesNotThrow(() -> target.delete(assignmentIdMock));

        verify(repo, times(1)).findById(assignmentIdMock);
        verify(repo, times(1)).delete(entityMock);
    }

    @Test
    void delete__RequestAssignmentNotFound__ThrowsException() {
        long assignmentIdMock = 1;

        when(repo.findById(assignmentIdMock)).thenReturn(Optional.empty());
        Assertions.assertThrows(RequestAssignmentNotFoundException.class, () -> target.delete(assignmentIdMock));

        verify(repo, times(1)).findById(assignmentIdMock);
        verifyNoMoreInteractions(repo);
    }
}