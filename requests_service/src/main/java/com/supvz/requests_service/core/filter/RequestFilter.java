package com.supvz.requests_service.core.filter;

import com.supvz.requests_service.model.entity.enums.RequestStatus;


/**
 * Схема фильтра для заявок.
 */
public record RequestFilter(
        Integer pvzId,
        Long appellantId,
        String subject,
        RequestStatus requestStatus
) {
}