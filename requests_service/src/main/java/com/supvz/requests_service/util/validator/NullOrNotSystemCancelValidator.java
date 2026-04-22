package com.supvz.requests_service.util.validator;

import com.supvz.requests_service.core.annotation.NullOrNotSystemCancel;
import com.supvz.requests_service.model.entity.enums.AssignmentAction;
import jakarta.validation.ConstraintValidator;
import jakarta.validation.ConstraintValidatorContext;

public class NullOrNotSystemCancelValidator implements ConstraintValidator<NullOrNotSystemCancel, AssignmentAction> {
    @Override
    public boolean isValid(AssignmentAction value, ConstraintValidatorContext constraintValidatorContext) {
        if (value == null) return true;
        return value != AssignmentAction.system_cancel;
    }
}