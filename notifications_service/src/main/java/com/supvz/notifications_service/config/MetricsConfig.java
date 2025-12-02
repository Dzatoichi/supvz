package com.supvz.notifications_service.config;

import io.micrometer.core.instrument.MeterRegistry;
import org.springframework.beans.factory.annotation.Value;
import org.springframework.boot.actuate.autoconfigure.metrics.MeterRegistryCustomizer;
import org.springframework.context.annotation.Bean;
import org.springframework.context.annotation.Configuration;

/**
 * <h3>
 * Конфигурация для метрик, вывода логов.
 * </h3>
 */
@Configuration
public class MetricsConfig {
    @Value("${spring.application.name}")
    private String applicationName;

    /**
     * Настройка для правильного парсинга логов.
     */
    @Bean
    MeterRegistryCustomizer<MeterRegistry> metricsCommonTags() {
        return registry -> registry.config().commonTags("application", applicationName);
    }
}
