package com.supvz.requests_service.util.validator;

import com.supvz.requests_service.core.annotation.EmptyOrSize;
import jakarta.validation.ConstraintValidator;
import jakarta.validation.ConstraintValidatorContext;

/**
 * Валидатор для аннотации {@link EmptyOrSize}.
 * Разрешает {@code null} или пустую строку, а также строки длиной в пределах [min, max].
 */
public class EmptyOrSizeValidator implements ConstraintValidator<EmptyOrSize, String> {
    private int max;
    private int min;

    /**
     * Инициализирует валидатор значениями из аннотации.
     *
     * @param constraintAnnotation аннотация {@link EmptyOrSize}
     */
    @Override
    public void initialize(EmptyOrSize constraintAnnotation) {
        this.max = constraintAnnotation.max();
        this.min = constraintAnnotation.min();
        ConstraintValidator.super.initialize(constraintAnnotation);
    }

    /**
     * Проверяет, что значение либо {@code null}/пустое, либо имеет допустимую длину.
     *
     * @param value   проверяемое значение
     * @param context контекст валидации
     * @return {@code true}, если значение валидно
     */
    @Override
    public boolean isValid(String value, ConstraintValidatorContext context) {
        if (value == null || value.isEmpty())
            return true;
        return value.length() >= min && value.length() <= max;
    }
}