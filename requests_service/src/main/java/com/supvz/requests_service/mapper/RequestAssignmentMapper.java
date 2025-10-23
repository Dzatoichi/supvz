package com.supvz.requests_service.mapper;

import com.supvz.requests_service.core.PageDto;
import com.supvz.requests_service.core.RequestAssignmentDto;
import com.supvz.requests_service.core.RequestAssignmentPayload;
import com.supvz.requests_service.core.RequestAssignmentUpdatePayload;
import com.supvz.requests_service.entity.Request;
import com.supvz.requests_service.entity.RequestAssignment;
import org.springframework.data.domain.Page;

/*
Интерфейс маппера для работы с ответами на запросы.
 */
public interface RequestAssignmentMapper {
    /*
    Метод для преобразования полезной нагрузки в сущность.
     */
    RequestAssignment create(Request request, RequestAssignmentPayload payload);

    /*
    Метод для преобразования ответа в ДТО.
     */
    RequestAssignmentDto read(RequestAssignment requestAssignment);

    /*
    Метод для преобразования springframework.data.Page в ДТО.
     */
    PageDto<RequestAssignmentDto> readPage(Page<RequestAssignment> page);

    /*
    Метод для преобразования сущности и полезной нагрузки для обновления в сущность.
     */
    RequestAssignment update(RequestAssignment found, RequestAssignmentUpdatePayload payload);
}
