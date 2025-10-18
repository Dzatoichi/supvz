package com.supvz.requests_service.service;

import com.supvz.requests_service.core.*;
import com.supvz.requests_service.entity.Request;
import com.supvz.requests_service.entity.RequestAssignment;
import com.supvz.requests_service.mapper.RequestAssignmentMapper;
import com.supvz.requests_service.repo.RequestAssignmentRepository;
import com.supvz.requests_service.service.impl.RequestAssignmentServiceImpl;
import org.junit.jupiter.api.Assertions;
import org.junit.jupiter.api.Test;
import org.junit.jupiter.api.extension.ExtendWith;
import org.mockito.InjectMocks;
import org.mockito.Mock;
import org.mockito.junit.jupiter.MockitoExtension;
import org.springframework.data.domain.Page;
import org.springframework.data.domain.PageRequest;
import org.springframework.data.domain.Pageable;

import java.util.Optional;
import java.util.UUID;

import static org.junit.jupiter.api.Assertions.*;
import static org.mockito.Mockito.*;

@ExtendWith(MockitoExtension.class)
class RequestAssignmentServiceTest {
    @InjectMocks
    private RequestAssignmentServiceImpl service;

    @Mock
    private RequestAssignmentMapper mapper;

    @Mock
    private RequestAssignmentRepository repo;

    @Mock
    private RequestService requestService;


    @Test
    void create__ReturnsRequestAssignmentDto() {
        long requestId = 1L;
        UUID handymanId = UUID.randomUUID();
        RequestAssignmentPayload payload = new RequestAssignmentPayload(handymanId, null);

        Request found = Request.builder().id(requestId).build();
        RequestAssignment mapped = RequestAssignment.builder().request(found).handymanId(handymanId).build();
        RequestAssignment saved = RequestAssignment.builder().id(1L).request(found).handymanId(handymanId).build();
        RequestAssignmentDto body = RequestAssignmentDto.builder()
                .id(1L)
                .requestId(requestId)
                .handymanId(handymanId)
                .build();

        when(requestService.get(requestId)).thenReturn(found);
        when(mapper.create(found, payload)).thenReturn(mapped);
        when(repo.save(mapped)).thenReturn(saved);
        when(mapper.read(saved)).thenReturn(body);

        RequestAssignmentDto result = assertDoesNotThrow(() -> service.create(requestId, payload));
        assertEquals(body, result);

        verify(requestService, times(1)).get(requestId);
        verify(mapper, times(1)).create(found, payload);
        verify(repo, times(1)).save(mapped);
        verify(mapper, times(1)).read(saved);
    }

    @Test
    void create__RequestNotFound__ThrowsException() {
        long requestId = 1L;
        UUID handymanId = UUID.randomUUID();
        RequestAssignmentPayload payload = new RequestAssignmentPayload(handymanId, null);

        when(requestService.get(requestId)).thenThrow(RequestNotFoundException.class);
        assertThrows(RequestNotFoundException.class, () -> service.create(requestId, payload));

        verify(requestService, times(1)).get(requestId);
        verifyNoInteractions(mapper, repo);
    }

    @Test
    void readAll__ReturnsPageDto() {
        int page = 0;
        int size = 5;
        long requestId = 1L;

        Pageable pageable = PageRequest.of(page, size);

        Page<RequestAssignment> found = Page.empty();
        PageDto<RequestAssignmentDto> body = PageDto.<RequestAssignmentDto>builder().build();

        when(repo.findAll(requestId, pageable)).thenReturn(found);
        when(mapper.readPage(found)).thenReturn(body);

        PageDto<RequestAssignmentDto> result = assertDoesNotThrow(() -> service.readAll(requestId, page, size));
        assertEquals(body, result);

        verify(repo, times(1)).findAll(requestId, pageable);
        verify(mapper, times(1)).readPage(found);
    }

    @Test
    void read__ReturnsRequestAssignmentDto() {
        long assignmentId = 1;

        RequestAssignment assignment = RequestAssignment.builder().id(assignmentId).build();
        RequestAssignmentDto body = RequestAssignmentDto.builder().id(assignmentId).build();

        when(repo.findById(assignmentId)).thenReturn(Optional.of(assignment));
        when(mapper.read(assignment)).thenReturn(body);

        RequestAssignmentDto result = Assertions.assertDoesNotThrow(() -> service.read(assignmentId));
        Assertions.assertEquals(body, result);

        verify(repo, times(1)).findById(assignmentId);
        verify(mapper, times(1)).read(assignment);
    }

    @Test
    void read__RequestAssignmentNotFound__ThrowsException() {
        long assignmentId = 1;

        when(repo.findById(assignmentId)).thenReturn(Optional.empty());
        Assertions.assertThrows(RequestAssignmentNotFoundException.class, () -> service.read(assignmentId));

        verify(repo, times(1)).findById(assignmentId);
        verifyNoInteractions(mapper);
    }


    @Test
    void update__ReturnsRequestDto() {
        long assignmentId = 1;
        UUID handymanId = UUID.randomUUID();
        Status status = Status.ASSIGNED;

        Status newStatus = Status.CONFIRMED;
        UUID newHandymanId = UUID.randomUUID();
        String newDescription = "newDescription";
        RequestAssignmentUpdatePayload payload = new RequestAssignmentUpdatePayload(newStatus, newHandymanId, newDescription);

        RequestAssignment found = RequestAssignment.builder()
                .id(assignmentId)
                .status(status)
                .handymanId(handymanId)
                .description(null)
                .build();
        RequestAssignment mapped = RequestAssignment.builder()
                .id(assignmentId)
                .status(newStatus)
                .handymanId(newHandymanId)
                .description(newDescription)
                .build();
        RequestAssignmentDto body = RequestAssignmentDto.builder()
                .id(assignmentId)
                .status(newStatus)
                .handymanId(newHandymanId)
                .description(newDescription)
                .build();

        when(repo.findById(assignmentId)).thenReturn(Optional.of(found));
        when(mapper.update(found, payload)).thenReturn(mapped);
        when(repo.save(mapped)).thenReturn(mapped);
        when(mapper.read(mapped)).thenReturn(body);

        RequestAssignmentDto result = Assertions.assertDoesNotThrow(() -> service.update(assignmentId, payload));
        Assertions.assertEquals(body, result);

        verify(repo, times(1)).findById(assignmentId);
        verify(mapper, times(1)).update(found, payload);
        verify(repo, times(1)).save(mapped);
        verify(mapper, times(1)).read(mapped);
    }


    @Test
    void update__RequestAssignmentNotFound__ThrowsException() {
        long assignmentId = 1;

        Status newStatus = Status.CONFIRMED;
        UUID newHandymanId = UUID.randomUUID();
        String newDescription = "newDescription";
        RequestAssignmentUpdatePayload payload = new RequestAssignmentUpdatePayload(newStatus, newHandymanId, newDescription);

        when(repo.findById(assignmentId)).thenReturn(Optional.empty());

        Assertions.assertThrows(RequestAssignmentNotFoundException.class, () -> service.update(assignmentId, payload));

        verify(repo, times(1)).findById(assignmentId);
        verifyNoInteractions(mapper);
        verifyNoMoreInteractions(repo);
    }

    @Test
    void delete__DoesNotThrowsException() {
        long assignmentId = 1;

        RequestAssignment request = RequestAssignment.builder().id(assignmentId).build();

        when(repo.findById(assignmentId)).thenReturn(Optional.of(request));

        Assertions.assertDoesNotThrow(() -> service.delete(assignmentId));

        verify(repo, times(1)).findById(assignmentId);
        verify(repo, times(1)).delete(request);
    }

    @Test
    void delete__RequestAssignmentNotFound__ThrowsException() {
        long assignmentId = 1;

        when(repo.findById(assignmentId)).thenReturn(Optional.empty());
        Assertions.assertThrows(RequestAssignmentNotFoundException.class, () -> service.delete(assignmentId));

        verify(repo, times(1)).findById(assignmentId);
        verifyNoMoreInteractions(repo);
    }

}