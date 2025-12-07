package com.supvz.requests_service.service;

import com.supvz.requests_service.core.exception.RequestNotFoundException;
import com.supvz.requests_service.core.filter.RequestFilter;
import com.supvz.requests_service.model.dto.*;
import com.supvz.requests_service.model.entity.Request;
import com.supvz.requests_service.mapper.entity.RequestMapper;
import com.supvz.requests_service.repo.RequestRepository;
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

import static org.mockito.Mockito.*;

@ExtendWith(MockitoExtension.class)
class RequestServiceTests {
    @InjectMocks
    private RequestEntityService target;
    @Mock
    private RequestMapper mapper;
    @Mock
    private RequestRepository repo;

    @Test
    void create__ReturnsRequestDto() {
        RequestPayload payload = mock(RequestPayload.class);
        Request mappedMock = mock(Request.class);
        Request savedMock = mock(Request.class);
        RequestDto dtoMock = mock(RequestDto.class);

        when(mapper.create(payload)).thenReturn(mappedMock);
        when(repo.save(mappedMock)).thenReturn(savedMock);
        when(mapper.read(savedMock)).thenReturn(dtoMock);

        RequestDto result = Assertions.assertDoesNotThrow(() -> target.create(payload));
        Assertions.assertEquals(dtoMock, result);

        verify(mapper, times(1)).create(payload);
        verify(repo, times(1)).save(mappedMock);
        verify(mapper, times(1)).read(savedMock);
    }

    @Test
    void readAll__ReturnsPageDto() {
        RequestFilter filterMock = mock(RequestFilter.class);
        Page<Request> pageMock = mock(Page.class);
        PageDto<RequestPlainDto> pageDtoMock = mock(PageDto.class);

        when(repo.findAll(any(Specification.class), any(Pageable.class))).thenReturn(pageMock);
        when(mapper.readPage(pageMock)).thenReturn(pageDtoMock);

        PageDto<RequestPlainDto> result = Assertions.assertDoesNotThrow(() -> target.readAll(1, 1, filterMock));
        Assertions.assertEquals(pageDtoMock, result);

        verify(repo, times(1)).findAll(any(Specification.class), any(Pageable.class));
        verify(mapper, times(1)).readPage(pageMock);
    }

    @Test
    void read__ReturnsRequestDto() {
        long requestIdMock = 1;
        Request entityMock = mock(Request.class);
        RequestDto dtoMock = mock(RequestDto.class);

        when(repo.findById(requestIdMock)).thenReturn(Optional.of(entityMock));
        when(mapper.read(entityMock)).thenReturn(dtoMock);

        RequestDto result = Assertions.assertDoesNotThrow(() -> target.read(requestIdMock));
        Assertions.assertEquals(dtoMock, result);

        verify(repo, times(1)).findById(requestIdMock);
        verify(mapper, times(1)).read(entityMock);
    }

    @Test
    void read__RequestNotFound__ThrowsException() {
        long requestIdMock = 1;

        when(repo.findById(requestIdMock)).thenReturn(Optional.empty());
        Assertions.assertThrows(RequestNotFoundException.class, () -> target.read(requestIdMock));

        verify(repo, times(1)).findById(requestIdMock);
        verifyNoInteractions(mapper);
    }

    @Test
    void update__ReturnsRequestDto() {
        long requestIdMock = 1;
        RequestUpdatePayload payload = mock(RequestUpdatePayload.class);
        Request found = mock(Request.class);
        Request mapped = mock(Request.class);
        RequestDto body = mock(RequestDto.class);

        when(repo.findById(requestIdMock)).thenReturn(Optional.of(found));
        when(mapper.update(found, payload)).thenReturn(mapped);
        when(repo.save(mapped)).thenReturn(mapped);
        when(mapper.read(mapped)).thenReturn(body);

        RequestDto result = Assertions.assertDoesNotThrow(() -> target.update(requestIdMock, payload));
        Assertions.assertEquals(body, result);

        verify(repo, times(1)).findById(requestIdMock);
        verify(mapper, times(1)).update(found, payload);
        verify(repo, times(1)).save(mapped);
        verify(mapper, times(1)).read(mapped);
    }


    @Test
    void update__RequestNotFound__ThrowsException() {
        long requestIdMock = 1;
        RequestUpdatePayload payloadMock = mock(RequestUpdatePayload.class);

        when(repo.findById(requestIdMock)).thenReturn(Optional.empty());

        Assertions.assertThrows(RequestNotFoundException.class, () -> target.update(requestIdMock, payloadMock));

        verify(repo, times(1)).findById(requestIdMock);
        verifyNoInteractions(mapper);
        verifyNoMoreInteractions(repo);
    }

    @Test
    void delete__DoesNotThrowsException() {
        long requestIdMock = 1;
        Request entityMock = Request.builder().id(requestIdMock).build();

        when(repo.findById(requestIdMock)).thenReturn(Optional.of(entityMock));

        Assertions.assertDoesNotThrow(() -> target.delete(requestIdMock));

        verify(repo, times(1)).findById(requestIdMock);
        verify(repo, times(1)).delete(entityMock);
    }

    @Test
    void delete__RequestNotFound__ThrowsException() {
        long requestIdMock = 1;

        when(repo.findById(requestIdMock)).thenReturn(Optional.empty());
        Assertions.assertThrows(RequestNotFoundException.class, () -> target.delete(requestIdMock));

        verify(repo, times(1)).findById(requestIdMock);
        verifyNoMoreInteractions(repo);
    }
}