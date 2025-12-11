package com.supvz.requests_service.service;

import com.supvz.requests_service.core.exception.RequestAssignmentInvalidPayloadException;
import com.supvz.requests_service.model.entity.enums.AssignmentAction;
import com.supvz.requests_service.model.entity.enums.RequestStatus;
import com.supvz.requests_service.core.exception.RequestAssignmentConflictException;
import com.supvz.requests_service.core.exception.RequestAssignmentNotFoundException;
import com.supvz.requests_service.core.exception.RequestNotFoundException;
import com.supvz.requests_service.core.filter.RequestAssignmentFilter;
import com.supvz.requests_service.model.dto.PageDto;
import com.supvz.requests_service.model.dto.RequestAssignmentDto;
import com.supvz.requests_service.model.dto.RequestAssignmentPayload;
import com.supvz.requests_service.model.dto.RequestAssignmentUpdatePayload;
import com.supvz.requests_service.model.entity.Request;
import com.supvz.requests_service.model.entity.RequestAssignment;
import com.supvz.requests_service.mapper.RequestAssignmentMapper;
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
import static org.junit.jupiter.api.Assertions.assertDoesNotThrow;
import static org.junit.jupiter.api.Assertions.assertThrows;
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
        int handymanIdMock = 1;
        RequestAssignmentPayload payloadMock = new RequestAssignmentPayload(requestIdMock, handymanIdMock, null);
        Request entityMock = mock(Request.class);
        RequestAssignment mappedMock = mock(RequestAssignment.class);
        RequestAssignment savedMock = mock(RequestAssignment.class);
        RequestAssignmentDto dtoMock = mock(RequestAssignmentDto.class);


        when(repo.existsByRequestIdAndHandymanId(requestIdMock, handymanIdMock)).thenReturn(false);
        when(requestService.assign(requestIdMock)).thenReturn(entityMock);
        when(mapper.create(entityMock, payloadMock)).thenReturn(mappedMock);
        when(repo.save(mappedMock)).thenReturn(savedMock);
        when(mapper.read(savedMock)).thenReturn(dtoMock);

        RequestAssignmentDto result = assertDoesNotThrow(() -> target.create(payloadMock));
        assertEquals(dtoMock, result);

        verify(repo, times(1)).existsByRequestIdAndHandymanId(requestIdMock, handymanIdMock);
        verify(requestService, times(1)).assign(requestIdMock);
        verify(mapper, times(1)).create(entityMock, payloadMock);
        verify(repo, times(1)).save(mappedMock);
        verify(mapper, times(1)).read(savedMock);
    }

    @Test
    void create__RequestNotFound__ThrowsException() {
        long requestIdMock = 1;
        int handymanIdMock = 1;
        RequestAssignmentPayload payloadMock = new RequestAssignmentPayload(requestIdMock, handymanIdMock, null);

        when(repo.existsByRequestIdAndHandymanId(requestIdMock, handymanIdMock)).thenReturn(false);
        when(requestService.assign(requestIdMock)).thenThrow(RequestNotFoundException.class);
        assertThrows(RequestNotFoundException.class, () -> target.create(payloadMock));

        verify(repo, times(1)).existsByRequestIdAndHandymanId(requestIdMock, handymanIdMock);
        verify(requestService, times(1)).assign(requestIdMock);
        verifyNoMoreInteractions(repo);
        verifyNoInteractions(mapper);
    }

    @Test
    void create__RequestAssignmentAlreadyExists__ThrowsException() {
        long requestIdMock = 1;
        int handymanIdMock = 1;
        RequestAssignmentPayload payloadMock = new RequestAssignmentPayload(requestIdMock, handymanIdMock, null);

        when(repo.existsByRequestIdAndHandymanId(requestIdMock, handymanIdMock)).thenReturn(true);
        assertThrows(RequestAssignmentConflictException.class, () -> target.create(payloadMock));

        verify(repo, times(1)).existsByRequestIdAndHandymanId(requestIdMock, handymanIdMock);
        verifyNoMoreInteractions(repo);
        verifyNoInteractions(mapper, requestService);
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

        RequestAssignmentDto result = assertDoesNotThrow(() -> target.read(assignmentIdMock));
        Assertions.assertEquals(dtoMock, result);

        verify(repo, times(1)).findById(assignmentIdMock);
        verify(mapper, times(1)).read(entityMock);
    }

    @Test
    void read__RequestAssignmentNotFound__ThrowsException() {
        long assignmentIdMock = 1;

        when(repo.findById(assignmentIdMock)).thenReturn(Optional.empty());
        assertThrows(RequestAssignmentNotFoundException.class, () -> target.read(assignmentIdMock));

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

        RequestAssignmentDto result = assertDoesNotThrow(() -> target.update(assignmentIdMock, payloadMock));
        Assertions.assertEquals(dtoMock, result);

        verify(repo, times(1)).findById(assignmentIdMock);
        verify(mapper, times(1)).update(entityMock, payloadMock);
        verify(repo, times(1)).save(entityMock);
        verify(mapper, times(1)).read(entityMock);
    }

    @Test
    void update__WithAction__ReturnsRequestDto() {
        long assignmentIdMock = 1;
        AssignmentAction actionMock = AssignmentAction.assign;
        RequestAssignmentUpdatePayload payloadMock = new RequestAssignmentUpdatePayload(actionMock, null, null);
        Request requestMock = Request.builder().id(1L).build();
        RequestAssignment assignmentMock = RequestAssignment.builder().id(assignmentIdMock).request(requestMock).build();
        RequestAssignmentDto dtoMock = mock(RequestAssignmentDto.class);

        when(repo.findById(assignmentIdMock)).thenReturn(Optional.of(assignmentMock));
        doNothing().when(requestService).setStatus(requestMock, actionMock.getTargetRequestStatus());
        when(mapper.update(assignmentMock, payloadMock)).thenReturn(assignmentMock);
        when(repo.save(assignmentMock)).thenReturn(assignmentMock);
        when(mapper.read(assignmentMock)).thenReturn(dtoMock);

        RequestAssignmentDto result = assertDoesNotThrow(() -> target.update(assignmentIdMock, payloadMock));
        Assertions.assertEquals(dtoMock, result);

        verify(repo, times(1)).findById(assignmentIdMock);
        verify(requestService, times(1)).setStatus(requestMock, actionMock.getTargetRequestStatus());
        verify(mapper, times(1)).update(assignmentMock, payloadMock);
        verify(repo, times(1)).save(assignmentMock);
        verify(mapper, times(1)).read(assignmentMock);
    }

    @Test
    void update__WithCancelActionAndRequestHasWorkers__RequestStatusUnchangedAndReturnsRequestDto() {
        long assignmentIdMock = 1;
        long requestIdMock = 2L;
        RequestStatus requestStatusMock = RequestStatus.assigned;
        AssignmentAction actionMock = AssignmentAction.self_cancel;
        RequestAssignmentUpdatePayload payloadMock = new RequestAssignmentUpdatePayload(actionMock, null, null);
        Request requestMock = Request.builder().id(requestIdMock).status(requestStatusMock).build();
        RequestAssignment assignmentMock = RequestAssignment.builder().id(assignmentIdMock).request(requestMock).build();
        RequestAssignmentDto dtoMock = mock(RequestAssignmentDto.class);

        when(repo.findById(assignmentIdMock)).thenReturn(Optional.of(assignmentMock));
        when(repo.existsByRequestIdAndActionAndIdNot(requestIdMock, AssignmentAction.assign, assignmentIdMock)).thenReturn(true);
        doNothing().when(requestService).setStatus(requestMock, requestStatusMock);
        when(mapper.update(assignmentMock, payloadMock)).thenReturn(assignmentMock);
        when(repo.save(assignmentMock)).thenReturn(assignmentMock);
        when(mapper.read(assignmentMock)).thenReturn(dtoMock);

        RequestAssignmentDto result = assertDoesNotThrow(() -> target.update(assignmentIdMock, payloadMock));
        Assertions.assertEquals(dtoMock, result);

        verify(repo, times(1)).findById(assignmentIdMock);
        verify(repo, times(1)).existsByRequestIdAndActionAndIdNot(requestIdMock, AssignmentAction.assign, assignmentIdMock);
        verify(requestService, times(1)).setStatus(requestMock, requestStatusMock);
        verify(mapper, times(1)).update(assignmentMock, payloadMock);
        verify(repo, times(1)).save(assignmentMock);
        verify(mapper, times(1)).read(assignmentMock);
    }

    @Test
    void update__WithCancelAction__ReturnsRequestDto() {
        long assignmentIdMock = 1;
        long requestIdMock = 2L;
        RequestStatus requestStatusMock = RequestStatus.assigned;
        AssignmentAction actionMock = AssignmentAction.self_cancel;
        RequestAssignmentUpdatePayload payloadMock = new RequestAssignmentUpdatePayload(actionMock, null, null);
        Request requestMock = Request.builder().id(requestIdMock).status(requestStatusMock).build();
        RequestAssignment assignmentMock = RequestAssignment.builder().id(assignmentIdMock).request(requestMock).build();
        RequestAssignmentDto dtoMock = mock(RequestAssignmentDto.class);

        when(repo.findById(assignmentIdMock)).thenReturn(Optional.of(assignmentMock));
        when(repo.existsByRequestIdAndActionAndIdNot(requestIdMock, AssignmentAction.assign, assignmentIdMock)).thenReturn(false);
        doNothing().when(requestService).setStatus(requestMock, actionMock.getTargetRequestStatus());
        when(mapper.update(assignmentMock, payloadMock)).thenReturn(assignmentMock);
        when(repo.save(assignmentMock)).thenReturn(assignmentMock);
        when(mapper.read(assignmentMock)).thenReturn(dtoMock);

        RequestAssignmentDto result = assertDoesNotThrow(() -> target.update(assignmentIdMock, payloadMock));
        Assertions.assertEquals(dtoMock, result);

        verify(repo, times(1)).findById(assignmentIdMock);
        verify(repo, times(1)).existsByRequestIdAndActionAndIdNot(requestIdMock, AssignmentAction.assign, assignmentIdMock);
        verify(requestService, times(1)).setStatus(requestMock, actionMock.getTargetRequestStatus());
        verify(mapper, times(1)).update(assignmentMock, payloadMock);
        verify(repo, times(1)).save(assignmentMock);
        verify(mapper, times(1)).read(assignmentMock);
    }


    @Test
    void update__RequestAssignmentNotFound__ThrowsException() {
        long assignmentIdMock = 1;
        RequestAssignmentUpdatePayload payloadMock = mock(RequestAssignmentUpdatePayload.class);

        when(repo.findById(assignmentIdMock)).thenReturn(Optional.empty());

        assertThrows(RequestAssignmentNotFoundException.class, () -> target.update(assignmentIdMock, payloadMock));

        verify(repo, times(1)).findById(assignmentIdMock);
        verifyNoInteractions(mapper);
        verifyNoMoreInteractions(repo);
    }

    @Test
    void update__WithSystemCancelAction__ThrowsRequestAssignmentInvalidPayloadException() {
        long assignmentIdMock = 1;
        Request requestMock = Request.builder().id(1L).build();
        RequestAssignment assignmentMock = RequestAssignment.builder()
                .id(assignmentIdMock)
                .request(requestMock)
                .build();
        RequestAssignmentUpdatePayload payloadMock = new RequestAssignmentUpdatePayload(
                AssignmentAction.system_cancel, null, null
        );

        when(repo.findById(assignmentIdMock)).thenReturn(Optional.of(assignmentMock));

        assertThrows(
                RequestAssignmentInvalidPayloadException.class,
                () -> target.update(assignmentIdMock, payloadMock)
        );

        verify(repo, times(1)).findById(assignmentIdMock);
        verifyNoInteractions(mapper, requestService);
    }

    @Test
    void update__WithCompleteAction__CancelsOtherActiveAssignmentsAndSetsRequestStatusToCompleted() {
        long assignmentIdMock = 1;
        long requestIdMock = 2L;
        Request requestMock = Request.builder().id(requestIdMock).build();
        RequestAssignment assignmentMock = RequestAssignment.builder()
                .id(assignmentIdMock)
                .request(requestMock)
                .build();
        RequestAssignmentUpdatePayload payloadMock = new RequestAssignmentUpdatePayload(
                AssignmentAction.complete, null, null
        );
        RequestAssignmentDto dtoMock = mock(RequestAssignmentDto.class);

        when(repo.findById(assignmentIdMock)).thenReturn(Optional.of(assignmentMock));
        when(repo.setActiveAssignmentsAsSystemCancelByRequestIdInsteadAssignmentId(requestIdMock, assignmentIdMock))
                .thenReturn(2);
        when(mapper.update(assignmentMock, payloadMock)).thenReturn(assignmentMock);
        when(repo.save(assignmentMock)).thenReturn(assignmentMock);
        when(mapper.read(assignmentMock)).thenReturn(dtoMock);
        doNothing().when(requestService).setStatus(requestMock, RequestStatus.completed);

        RequestAssignmentDto result = assertDoesNotThrow(() ->
                target.update(assignmentIdMock, payloadMock)
        );
        Assertions.assertEquals(dtoMock, result);

        verify(repo, times(1)).findById(assignmentIdMock);
        verify(repo, times(1)).setActiveAssignmentsAsSystemCancelByRequestIdInsteadAssignmentId(requestIdMock, assignmentIdMock);
        verify(mapper, times(1)).update(assignmentMock, payloadMock);
        verify(repo, times(1)).save(assignmentMock);
        verify(mapper, times(1)).read(assignmentMock);
        verify(requestService, times(1)).setStatus(requestMock, RequestStatus.completed);
    }

    @Test
    void update__WithRejectAction__CancelsOtherActiveAssignmentsAndSetsRequestStatusToRejected() {
        long assignmentIdMock = 1;
        long requestIdMock = 2L;
        Request requestMock = Request.builder().id(requestIdMock).build();
        RequestAssignment assignmentMock = RequestAssignment.builder()
                .id(assignmentIdMock)
                .request(requestMock)
                .build();
        RequestAssignmentUpdatePayload payloadMock = new RequestAssignmentUpdatePayload(
                AssignmentAction.reject, null, null
        );
        RequestAssignmentDto dtoMock = mock(RequestAssignmentDto.class);

        when(repo.findById(assignmentIdMock)).thenReturn(Optional.of(assignmentMock));
        when(repo.setActiveAssignmentsAsSystemCancelByRequestIdInsteadAssignmentId(requestIdMock, assignmentIdMock))
                .thenReturn(1);
        when(mapper.update(assignmentMock, payloadMock)).thenReturn(assignmentMock);
        when(repo.save(assignmentMock)).thenReturn(assignmentMock);
        when(mapper.read(assignmentMock)).thenReturn(dtoMock);
        doNothing().when(requestService).setStatus(requestMock, RequestStatus.rejected);

        RequestAssignmentDto result = assertDoesNotThrow(() ->
                target.update(assignmentIdMock, payloadMock)
        );
        Assertions.assertEquals(dtoMock, result);

        verify(repo, times(1)).findById(assignmentIdMock);
        verify(repo, times(1)).setActiveAssignmentsAsSystemCancelByRequestIdInsteadAssignmentId(requestIdMock, assignmentIdMock);
        verify(mapper, times(1)).update(assignmentMock, payloadMock);
        verify(repo, times(1)).save(assignmentMock);
        verify(mapper, times(1)).read(assignmentMock);
        verify(requestService, times(1)).setStatus(requestMock, RequestStatus.rejected);
    }

    @Test
    void update__WithCompleteActionAndNoOtherActiveAssignments__SetsRequestStatusToCompletedWithoutCanceling() {
        long assignmentIdMock = 1;
        long requestIdMock = 2L;
        Request requestMock = Request.builder().id(requestIdMock).build();
        RequestAssignment assignmentMock = RequestAssignment.builder()
                .id(assignmentIdMock)
                .request(requestMock)
                .build();
        RequestAssignmentUpdatePayload payloadMock = new RequestAssignmentUpdatePayload(
                AssignmentAction.complete, null, null
        );
        RequestAssignmentDto dtoMock = mock(RequestAssignmentDto.class);

        when(repo.findById(assignmentIdMock)).thenReturn(Optional.of(assignmentMock));
        when(repo.setActiveAssignmentsAsSystemCancelByRequestIdInsteadAssignmentId(requestIdMock, assignmentIdMock))
                .thenReturn(0);
        when(mapper.update(assignmentMock, payloadMock)).thenReturn(assignmentMock);
        when(repo.save(assignmentMock)).thenReturn(assignmentMock);
        when(mapper.read(assignmentMock)).thenReturn(dtoMock);
        doNothing().when(requestService).setStatus(requestMock, RequestStatus.completed);

        RequestAssignmentDto result = assertDoesNotThrow(() ->
                target.update(assignmentIdMock, payloadMock)
        );
        Assertions.assertEquals(dtoMock, result);

        verify(repo, times(1)).findById(assignmentIdMock);
        verify(repo, times(1)).setActiveAssignmentsAsSystemCancelByRequestIdInsteadAssignmentId(requestIdMock, assignmentIdMock);
        verify(mapper, times(1)).update(assignmentMock, payloadMock);
        verify(repo, times(1)).save(assignmentMock);
        verify(mapper, times(1)).read(assignmentMock);
        verify(requestService, times(1)).setStatus(requestMock, RequestStatus.completed);
    }
}