package com.supvz.requests_service.model.dto;

import io.swagger.v3.oas.annotations.media.Schema;
import lombok.Builder;

import java.util.List;

@Builder
@Schema(description = "Стандартный объект пагинации")
public record PageDto<T>(
        @Schema(description = "Список элементов на текущей странице")
        List<T> content,

        @Schema(description = "Номер текущей страницы (начиная с 0)", example = "0")
        int page,

        @Schema(description = "Размер страницы", example = "10")
        int size,

        @Schema(description = "Общее количество элементов", example = "42")
        int total,

        @Schema(description = "Есть ли следующая страница")
        boolean hasNext,

        @Schema(description = "Есть ли предыдущая страница")
        boolean hasPrev
) {
}