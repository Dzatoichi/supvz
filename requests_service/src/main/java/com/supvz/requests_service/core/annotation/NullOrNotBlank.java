package com.supvz.requests_service.core.annotation;

import com.supvz.requests_service.util.validator.NullOrNotBlankValidator;
import jakarta.validation.Constraint;
import jakarta.validation.Payload;

import java.lang.annotation.ElementType;
import java.lang.annotation.Retention;
import java.lang.annotation.RetentionPolicy;
import java.lang.annotation.Target;

@Target(ElementType.FIELD)
@Retention(RetentionPolicy.RUNTIME)
@Constraint(validatedBy = NullOrNotBlankValidator.class)
public @interface NullOrNotBlank {
    String message() default "Поле должно быть либо пустым либо не состоять из пробельных символов.";
    Class<?>[] groups() default {};
    Class<? extends Payload>[] payload() default {};
}
