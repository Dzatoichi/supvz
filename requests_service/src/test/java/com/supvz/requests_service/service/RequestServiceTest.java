package com.supvz.requests_service.service;

import com.supvz.requests_service.core.*;
import com.supvz.requests_service.entity.Request;
import com.supvz.requests_service.mapper.RequestMapper;
import com.supvz.requests_service.repo.RequestRepository;
import com.supvz.requests_service.service.impl.RequestServiceImpl;
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

import static org.mockito.Mockito.*;

@ExtendWith(MockitoExtension.class)
class RequestServiceTest {
    @InjectMocks
    private RequestServiceImpl service;

    @Mock
    private RequestMapper mapper;

    @Mock
    private RequestRepository repo;

    @Test
    void create__ReturnsRequestDto() {
        long reqId = 1L;
        int pvzId = 1;
        UUID appellantId = UUID.randomUUID();

        RequestPayload payload = new RequestPayload(pvzId, appellantId, null);

        Request mapped = Request.builder()
                .pvzId(pvzId).appellantId(appellantId)
                .build();

        Request saved = Request.builder()
                .id(reqId)
                .pvzId(pvzId)
                .appellantId(appellantId)
                .build();

        RequestDto body = RequestDto.builder()
                .id(reqId)
                .pvzId(pvzId)
                .appellantId(appellantId)
                .build();

        when(mapper.create(payload)).thenReturn(mapped);
        when(repo.save(mapped)).thenReturn(saved);
        when(mapper.read(saved)).thenReturn(body);

        RequestDto result = Assertions.assertDoesNotThrow(() -> service.create(payload));

        Assertions.assertEquals(body, result);

        verify(mapper, times(1)).create(payload);
        verify(repo, times(1)).save(mapped);
        verify(mapper, times(1)).read(saved);
    }

    @Test
    void readAll__ReturnsPageDto() {
        int page = 0;
        int size = 5;
        RequestFilter filter = RequestFilter.builder().build();

        Pageable pageable = PageRequest.of(page, size);

        Page<Request> found = Page.empty();
        PageDto<RequestDto> body = PageDto.<RequestDto>builder().build();

        when(repo.findAll(null, null, pageable)).thenReturn(found);
        when(mapper.readPage(found)).thenReturn(body);

        PageDto<RequestDto> result = Assertions.assertDoesNotThrow(() -> service.readAll(page, size, filter));
        Assertions.assertEquals(body, result);

        verify(repo, times(1)).findAll(null, null, pageable);
        verify(mapper, times(1)).readPage(found);
    }

    @Test
    void read__ReturnsRequestDto() {
        long reqId = 1;

        Request request = Request.builder().id(reqId).build();
        RequestDto body = RequestDto.builder().id(reqId).build();

        when(repo.findById(reqId)).thenReturn(Optional.of(request));
        when(mapper.read(request)).thenReturn(body);

        RequestDto result = Assertions.assertDoesNotThrow(() -> service.read(reqId));
        Assertions.assertEquals(body, result);

        verify(repo, times(1)).findById(reqId);
        verify(mapper, times(1)).read(request);
    }

    @Test
    void read__RequestNotFound__ThrowsException() {
        long reqId = 1;

        when(repo.findById(reqId)).thenReturn(Optional.empty());
        Assertions.assertThrows(RequestNotFoundException.class, () -> service.read(reqId));

        verify(repo, times(1)).findById(reqId);
        verifyNoInteractions(mapper);
    }

    @Test
    void update__ReturnsRequestDto() {
        long reqId = 1;

        int pvzId = 1;
        int newPvzId = 2;
        String newDescription = "newDescription";
        RequestUpdatePayload payload = new RequestUpdatePayload(newPvzId, newDescription);

        Request found = Request.builder()
                .id(reqId)
                .pvzId(pvzId)
                .description(null)
                .build();
        Request mapped = Request.builder()
                .id(reqId)
                .pvzId(newPvzId)
                .description(newDescription)
                .build();
        RequestDto body = RequestDto.builder()
                .id(reqId)
                .pvzId(newPvzId)
                .description(newDescription)
                .build();

        when(repo.findById(reqId)).thenReturn(Optional.of(found));
        when(mapper.update(found, payload)).thenReturn(mapped);
        when(repo.save(mapped)).thenReturn(mapped);
        when(mapper.read(mapped)).thenReturn(body);

        RequestDto result = Assertions.assertDoesNotThrow(() -> service.update(reqId, payload));
        Assertions.assertEquals(body, result);

        verify(repo, times(1)).findById(reqId);
        verify(mapper, times(1)).update(found, payload);
        verify(repo, times(1)).save(mapped);
        verify(mapper, times(1)).read(mapped);
    }


    @Test
    void update__RequestNotFound__ThrowsException() {
        long reqId = 1;

        int newPvzId = 2;
        String newDescription = "newDescription";
        RequestUpdatePayload payload = new RequestUpdatePayload(newPvzId, newDescription);

        when(repo.findById(reqId)).thenReturn(Optional.empty());

        Assertions.assertThrows(RequestNotFoundException.class, () -> service.update(reqId, payload));

        verify(repo, times(1)).findById(reqId);
        verifyNoInteractions(mapper);
        verifyNoMoreInteractions(repo);
    }

    @Test
    void delete__DoesNotThrowsException() {
        long reqId = 1;

        Request request = Request.builder().id(reqId).build();

        when(repo.findById(reqId)).thenReturn(Optional.of(request));

        Assertions.assertDoesNotThrow(() -> service.delete(reqId));

        verify(repo, times(1)).findById(reqId);
        verify(repo, times(1)).delete(request);
    }

    @Test
    void delete__RequestNotFound__ThrowsException() {
        long reqId = 1;

        when(repo.findById(reqId)).thenReturn(Optional.empty());
        Assertions.assertThrows(RequestNotFoundException.class, () -> service.delete(reqId));

        verify(repo, times(1)).findById(reqId);
        verifyNoMoreInteractions(repo);
    }
}