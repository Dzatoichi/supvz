package com.supvz.requests_service.util.validator;

import com.supvz.requests_service.core.annotation.NullOrNotBlank;
import jakarta.validation.ConstraintValidator;
import jakarta.validation.ConstraintValidatorContext;

/**
 * Валидатор для аннотации {@link NullOrNotBlank}.
 * Разрешает {@code null}, но запрещает пустые или содержащие только пробелы строки.
 */
public class NullOrNotBlankValidator implements ConstraintValidator<NullOrNotBlank, String> {
    /**
     * Проверяет, что значение либо {@code null}, либо не пустое и не состоит только из пробелов.
     *
     * @param value   проверяемое значение
     * @param context контекст валидации
     * @return {@code true}, если значение валидно
     */
    @Override
    public boolean isValid(String value, ConstraintValidatorContext context) {
        if (value == null) return true;
        return !value.isBlank();
    }
}