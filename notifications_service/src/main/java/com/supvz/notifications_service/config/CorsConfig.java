package com.supvz.notifications_service.config;

import org.springframework.beans.factory.annotation.Value;
import org.springframework.context.annotation.Bean;
import org.springframework.context.annotation.Configuration;
import org.springframework.web.cors.CorsConfiguration;
import org.springframework.web.cors.CorsConfigurationSource;
import org.springframework.web.cors.UrlBasedCorsConfigurationSource;

import java.util.List;

/**
 * <h3>
 * Конфигурация CORS.
 * </h3>
 */
@Configuration
public class CorsConfig {
    @Value("${app.cors.allowed-origins}")
    private String[] allowedOrigins;
    @Value("${app.cors.allow-credentials}")
    private Boolean allowCredentials;
    @Value("${app.cors.allowed-methods}")
    private String[] allowedMethods;

    /**
     * Настройка CORS.
     * @return CorsConfigurationSource - бин, что и отвечает за обработку запросов с браузера.
     */
    @Bean
    public CorsConfigurationSource corsConfigurationSource() {
        CorsConfiguration configuration = new CorsConfiguration();
        configuration.setAllowedOrigins(List.of(allowedOrigins));
        configuration.setAllowedMethods(List.of(allowedMethods));
        configuration.setAllowCredentials(allowCredentials);
        configuration.setAllowedHeaders(List.of("*"));
        UrlBasedCorsConfigurationSource source = new UrlBasedCorsConfigurationSource();
        source.registerCorsConfiguration("/**", configuration);
        return source;
    }
}