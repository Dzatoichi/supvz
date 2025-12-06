package com.supvz.requests_service.model.dto;

import lombok.Builder;

import java.util.List;

@Builder
/*
ДТО страницы
 */
public record PageDto<T>(
        List<T> content,
        int page,
        int size,
        int total,
        boolean hasNext,
        boolean hasPrev
) {
}
