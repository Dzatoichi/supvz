package com.supvz.requests_service.core.annotation;

import com.supvz.requests_service.util.validator.NullOrNotSystemCancelValidator;
import jakarta.validation.Constraint;
import jakarta.validation.Payload;

import java.lang.annotation.ElementType;
import java.lang.annotation.Retention;
import java.lang.annotation.RetentionPolicy;
import java.lang.annotation.Target;

@Target(ElementType.FIELD)
@Retention(RetentionPolicy.RUNTIME)
@Constraint(validatedBy = NullOrNotSystemCancelValidator.class)
public @interface NullOrNotSystemCancel {
    String message() default ("Поле 'action' не может быть 'system_cancel'.");
    Class<?>[] groups() default {};
    Class<? extends Payload>[] payload() default {};
}
