package com.supvz.requests_service.core.filter;

import com.supvz.requests_service.core.enums.Status;
import lombok.Builder;

import java.util.UUID;


/**
 * Схема (Payload) для фильтрации заявок.
 */
@Builder
public record RequestFilter(
        Integer pvzId,
        Long appellantId,
        Status status
) {
}
// TODO: подумать еще о параметрах фильтрации.