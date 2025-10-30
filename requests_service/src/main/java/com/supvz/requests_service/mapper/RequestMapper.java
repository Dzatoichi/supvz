package com.supvz.requests_service.mapper;

import com.supvz.requests_service.core.PageDto;
import com.supvz.requests_service.core.RequestDto;
import com.supvz.requests_service.core.RequestPayload;
import com.supvz.requests_service.core.RequestUpdatePayload;
import com.supvz.requests_service.entity.Request;
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

    /*
    Метод для преобразования Page из springframework.data.Page в ДТО
     */
    PageDto<RequestDto> readPage(Page<Request> page);

    /*
    Метод для преобразования сущности и полезной нагрузки для обновления в сущность.
     */
    Request update(Request found, RequestUpdatePayload payload);
}
