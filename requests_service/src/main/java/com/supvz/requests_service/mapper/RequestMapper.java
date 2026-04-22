package com.supvz.requests_service.mapper;

import com.supvz.requests_service.model.entity.enums.RequestStatus;
import com.supvz.requests_service.model.dto.*;
import com.supvz.requests_service.model.entity.Request;
import org.springframework.data.domain.Page;

/*
Интерфейс маппера для работы с запросами.
 */
public interface RequestMapper {
    /*
    Метод для преобразования полезной нагрузки в сущность.
     */
    Request create(RequestPayload payload);

    /*
    Метод для преобразования сущности в ДТО.
     */
    RequestDto read(Request request);

    RequestPlainDto readPlain(Request request);

    /*
    Метод для преобразования Page из springframework.data.Page в ДТО
     */
    PageDto<RequestPlainDto> readPage(Page<Request> page);

    /*
    Метод для преобразования сущности и полезной нагрузки для обновления в сущность.
     */
    Request update(Request found, RequestUpdatePayload payload);

    Request setStatus(Request request, RequestStatus newStatus);
}
