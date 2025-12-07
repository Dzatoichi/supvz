package com.supvz.requests_service.controller;

import com.fasterxml.jackson.databind.ObjectMapper;
import com.supvz.requests_service.model.dto.RequestDto;
import com.supvz.requests_service.core.exception.RequestNotFoundException;
import com.supvz.requests_service.model.dto.RequestUpdatePayload;
import com.supvz.requests_service.service.RequestService;
import org.junit.jupiter.api.Test;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.boot.test.autoconfigure.web.servlet.WebMvcTest;
import org.springframework.http.MediaType;
import org.springframework.test.context.bean.override.mockito.MockitoBean;
import org.springframework.test.web.servlet.MockMvc;

import static org.mockito.Mockito.*;
import static org.springframework.test.web.servlet.request.MockMvcRequestBuilders.*;
import static org.springframework.test.web.servlet.result.MockMvcResultMatchers.content;
import static org.springframework.test.web.servlet.result.MockMvcResultMatchers.status;

@WebMvcTest(controllers = RequestController.class)
class RequestControllerTest {
    @Autowired
    private MockMvc mvc;
    @Autowired
    private ObjectMapper objectMapper;
    @MockitoBean
    private RequestService service;
    private static final String URI = "/api/v1/requests/%s";


    @Test
    void read__ReturnsOk() throws Exception {
        RequestDto dtoMock = mock(RequestDto.class);

        when(service.read(1)).thenReturn(dtoMock);

        mvc.perform(get(URI.formatted(1)))
                .andExpect(status().isOk())
                .andExpect(content().json(objectMapper.writeValueAsString(dtoMock)));

        verify(service, times(1)).read(1);
    }

    @Test
    void read__RequestNotFound__ReturnsBadRequest() throws Exception {
        when(service.read(1)).thenThrow(new RequestNotFoundException("mockMessage"));

        mvc.perform(get(URI.formatted(1))).andExpect(status().isBadRequest());

        verify(service, times(1)).read(1);
    }

    @Test
    void update__ReturnsOk() throws Exception {
        RequestUpdatePayload payloadMock = new RequestUpdatePayload(null, null, null);
        RequestDto dtoMock = new RequestDto(1, 1, 1, null, null, null);

        when(service.update(1, payloadMock)).thenReturn(dtoMock);

        mvc.perform(patch(URI.formatted(1))
                        .contentType(MediaType.APPLICATION_JSON)
                        .content(objectMapper.writeValueAsString(payloadMock)))
                .andExpect(status().isOk())
                .andExpect(content().json(objectMapper.writeValueAsString(dtoMock)));

        verify(service, times(1)).update(1, payloadMock);
    }

    @Test
    void update__RequestNotFound__ReturnsBadRequest() throws Exception {
        RequestUpdatePayload payload = new RequestUpdatePayload(null, null, null);

        when(service.update(1, payload)).thenThrow(new RequestNotFoundException("messageMock"));

        mvc.perform(patch(URI.formatted(1))
                        .contentType(MediaType.APPLICATION_JSON)
                        .content(objectMapper.writeValueAsString(payload)))
                .andExpect(status().isBadRequest());

        verify(service, times(1)).update(1, payload);
    }

    @Test
    void update__InvalidPayloadSubject__ReturnsBadRequest() throws Exception {
        RequestUpdatePayload payload = new RequestUpdatePayload(null, "  ", null);

        when(service.update(1, payload)).thenThrow(new RequestNotFoundException("messageMock"));

        mvc.perform(patch(URI.formatted(1))
                        .contentType(MediaType.APPLICATION_JSON)
                        .content(objectMapper.writeValueAsString(payload)))
                .andExpect(status().isBadRequest());

        verifyNoInteractions(service);
    }

    @Test
    void update__InvalidPayloadDescription__ReturnsBadRequest() throws Exception {
        RequestUpdatePayload payload = new RequestUpdatePayload(null, null, "  ");

        when(service.update(1, payload)).thenThrow(new RequestNotFoundException("messageMock"));

        mvc.perform(patch(URI.formatted(1))
                        .contentType(MediaType.APPLICATION_JSON)
                        .content(objectMapper.writeValueAsString(payload)))
                .andExpect(status().isBadRequest());

        verifyNoInteractions(service);
    }

    @Test
    void delete__ReturnsNoContent() throws Exception {
        mvc.perform(delete(URI.formatted(1))).andExpect(status().isNoContent());

        verify(service, times(1)).delete(1);
    }

    @Test
    void delete__RequestNotFound__ReturnsBadRequest() throws Exception {
        doThrow(new RequestNotFoundException("messageMock")).when(service).delete(1);

        mvc.perform(delete(URI.formatted(1)))
                .andExpect(status().isBadRequest());

        verify(service, times(1)).delete(1);
    }
}