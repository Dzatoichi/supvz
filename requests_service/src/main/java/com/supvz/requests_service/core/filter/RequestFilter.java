package com.supvz.requests_service.core.filter;

import com.supvz.requests_service.core.enums.RequestStatus;
import lombok.Builder;


/**
 * Схема (Payload) для фильтрации заявок.
 */
@Builder
public record RequestFilter(
        Integer pvzId,
        Long appellantId,
        RequestStatus requestStatus
) {
}
// TODO: подумать еще о параметрах фильтрации.