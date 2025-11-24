package com.supvz.notifications_service.config;

import com.fasterxml.jackson.databind.ObjectMapper;
import com.fasterxml.jackson.datatype.jsr310.JavaTimeModule;
import org.springframework.context.annotation.Bean;
import org.springframework.context.annotation.Configuration;
import org.springframework.retry.annotation.EnableRetry;
import org.springframework.scheduling.annotation.EnableAsync;
import org.springframework.scheduling.annotation.EnableScheduling;

import java.util.concurrent.Executor;
import java.util.concurrent.Executors;

import static com.fasterxml.jackson.databind.DeserializationFeature.READ_UNKNOWN_ENUM_VALUES_AS_NULL;

@Configuration
@EnableScheduling
@EnableRetry
@EnableAsync
public class AppConfig {

    @Bean
    public ObjectMapper objectMapper() {
        return new ObjectMapper()
                .enable(READ_UNKNOWN_ENUM_VALUES_AS_NULL)
                .registerModule(new JavaTimeModule());
    }

    @Bean
    public Executor inboxProcessingExecutor() {
        return Executors.newCachedThreadPool();
    }

    @Bean
    public Executor inboxCleaningExecutor() {
        return Executors.newCachedThreadPool();
    }

    @Bean("notificationProcessingExecutor")
    public Executor notificationProcessingExecutor() {
        return Executors.newFixedThreadPool(10);
    }

//    todo: cachedThreadPool опасен, создает беск. колво потоков
}
