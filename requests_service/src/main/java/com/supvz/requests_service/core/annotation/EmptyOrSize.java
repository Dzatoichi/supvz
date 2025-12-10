package com.supvz.requests_service.core.annotation;

import com.supvz.requests_service.util.validator.EmptyOrSizeValidator;
import jakarta.validation.Constraint;
import jakarta.validation.Payload;

import java.lang.annotation.ElementType;
import java.lang.annotation.Retention;
import java.lang.annotation.RetentionPolicy;
import java.lang.annotation.Target;

@Target(ElementType.FIELD)
@Retention(RetentionPolicy.RUNTIME)
@Constraint(validatedBy = EmptyOrSizeValidator.class)
public @interface EmptyOrSize {
    String message() default "Поле должно быть либо пустым либо подходить под условия минимальной {min} и максимальной длины {max}.";
    Class<?>[] groups() default {};
    Class<? extends Payload>[] payload() default {};
    int min();
    int max();
}
