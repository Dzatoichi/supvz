package com.supvz.requests_service.controller;

import com.fasterxml.jackson.databind.ObjectMapper;
import com.supvz.requests_service.core.RequestDto;
import com.supvz.requests_service.core.RequestNotFoundException;
import com.supvz.requests_service.core.RequestUpdatePayload;
import com.supvz.requests_service.service.RequestService;
import org.junit.jupiter.api.Test;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.boot.test.autoconfigure.web.servlet.WebMvcTest;
import org.springframework.http.MediaType;
import org.springframework.test.context.bean.override.mockito.MockitoBean;
import org.springframework.test.web.servlet.MockMvc;
import org.springframework.test.web.servlet.request.MockMvcRequestBuilders;

import static org.junit.jupiter.api.Assertions.*;
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
        int id = 1;
        RequestDto body = RequestDto.builder()
                .id(id)
                .build();

        when(service.read(id)).thenReturn(RequestDto.builder()
                .id(id)
                .build());

        mvc.perform(get(URI.formatted(id)))
                .andExpect(status().isOk())
                .andExpect(content().json(objectMapper.writeValueAsString(body)));

        verify(service, times(1)).read(id);
    }

    @Test
    void read__RequestNotFound__ReturnsBadRequest() throws Exception {
        int id = 1;

        when(service.read(id)).thenThrow(new RequestNotFoundException("test"));

        mvc.perform(get(URI.formatted(id)))
                .andExpect(status().isBadRequest());

        verify(service, times(1)).read(id);
    }

    @Test
    void update__ReturnsOk() throws Exception {
        int id = 1;

        int newPvzId = 2;
        String newDescription = "new";
        RequestUpdatePayload payload = new RequestUpdatePayload(newPvzId, newDescription);

        RequestDto body = RequestDto.builder()
                .id(id)
                .pvzId(newPvzId)
                .description(newDescription)
                .build();

        when(service.update(id, payload)).thenReturn(RequestDto.builder()
                .id(id)
                .pvzId(newPvzId)
                .description(newDescription)
                .build());

        mvc.perform(patch(URI.formatted(id))
                        .contentType(MediaType.APPLICATION_JSON)
                        .content(objectMapper.writeValueAsString(payload)))
                .andExpect(status().isOk())
                .andExpect(content().json(objectMapper.writeValueAsString(body)));

        verify(service, times(1)).update(id, payload);
    }

    @Test
    void update__RequestNotFound__ReturnsBadRequest() throws Exception {
        int id = 1;

        int newPvzId = 2;
        String newDescription = "new";
        RequestUpdatePayload payload = new RequestUpdatePayload(newPvzId, newDescription);

        when(service.update(id, payload)).thenThrow(new RequestNotFoundException("test"));

        mvc.perform(patch(URI.formatted(id))
                        .contentType(MediaType.APPLICATION_JSON)
                        .content(objectMapper.writeValueAsString(payload)))
                .andExpect(status().isBadRequest());

        verify(service, times(1)).update(id, payload);
    }

    @Test
    void delete__ReturnsNoContent() throws Exception {
        int id = 1;

        mvc.perform(delete(URI.formatted(id)))
                .andExpect(status().isNoContent());

        verify(service, times(1)).delete(id);
    }

    @Test
    void delete__RequestNotFound__ReturnsBadRequest() throws Exception {
        int id = 1;

        doThrow(new RequestNotFoundException("test")).when(service).delete(id);

        mvc.perform(delete(URI.formatted(id)))
                .andExpect(status().isBadRequest());

        verify(service, times(1)).delete(id);
    }
}