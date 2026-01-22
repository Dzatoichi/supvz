package com.supvz.requests_service.model.dto;

import io.swagger.v3.oas.annotations.media.Schema;
import com.supvz.requests_service.core.annotation.NullOrNotBlank;
import com.supvz.requests_service.core.annotation.NullOrNotSystemCancel;
import com.supvz.requests_service.model.entity.enums.AssignmentAction;

@Schema(description = "Частичное обновление обращения на заявку")
public record RequestAssignmentUpdatePayload(
        @Schema(description = "Новое действие (не может быть CANCEL, если не системное)", nullable = true)
        @NullOrNotSystemCancel
        AssignmentAction action,
        @Schema(description = "Обновлённый комментарий", nullable = true)
        @NullOrNotBlank
        String comment
) {}