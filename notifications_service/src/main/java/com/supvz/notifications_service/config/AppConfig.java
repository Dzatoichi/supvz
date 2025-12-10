package com.supvz.notifications_service.config;

import com.fasterxml.jackson.databind.ObjectMapper;
import com.fasterxml.jackson.datatype.jsr310.JavaTimeModule;
import org.springframework.beans.factory.annotation.Value;
import org.springframework.context.annotation.Bean;
import org.springframework.context.annotation.Configuration;
import org.springframework.retry.annotation.EnableRetry;
import org.springframework.scheduling.annotation.EnableAsync;
import org.springframework.scheduling.annotation.EnableScheduling;
import org.springframework.scheduling.concurrent.ThreadPoolTaskExecutor;

import java.util.concurrent.Executor;
import java.util.concurrent.ThreadPoolExecutor;

import static com.fasterxml.jackson.databind.DeserializationFeature.READ_UNKNOWN_ENUM_VALUES_AS_NULL;

/**
 * <h3>
 * Конфигурация приложения.
 * </h3>
 */
@Configuration
@EnableScheduling
@EnableRetry
@EnableAsync
public class AppConfig {
    @Value("${app.inbox.thread.core-pool-size}")
    private Integer inboxCorePoolSize;
    @Value("${app.inbox.thread.max-pool-size}")
    private Integer inboxMaxPoolSize;
    @Value("${app.inbox.thread.queue-capacity}")
    private Integer inboxQueueCapacity;
    @Value("${app.inbox.thread.name-prefix:notification-}")
    private String inboxThreadNamePrefix;
    @Value("${app.inbox.thread.wait-tasks-shutdown:true}")
    private Boolean inboxWaitTasksShutdown;
    @Value("${app.inbox.thread.await-termination-sec:60}")
    private Integer inboxAwaitTerminationSeconds;

    /**
     * Инициализация маппера для сериализации.
     * @return ObjectMapper - бин маппера
     */
    @Bean
    public ObjectMapper objectMapper() {
        return new ObjectMapper()
                .enable(READ_UNKNOWN_ENUM_VALUES_AS_NULL)
                .registerModule(new JavaTimeModule());
    }

    /**
     * Бин executor для управления потоками обработки inbox событий.
     */
    @Bean
    public Executor eventExecutor() {
        ThreadPoolTaskExecutor executor = new ThreadPoolTaskExecutor();
        executor.setCorePoolSize(inboxCorePoolSize);
        executor.setMaxPoolSize(inboxMaxPoolSize);
        executor.setQueueCapacity(inboxQueueCapacity);
        executor.setThreadNamePrefix(inboxThreadNamePrefix);
        executor.setWaitForTasksToCompleteOnShutdown(inboxWaitTasksShutdown);
        executor.setAwaitTerminationSeconds(inboxAwaitTerminationSeconds);
        executor.setRejectedExecutionHandler(new ThreadPoolExecutor.CallerRunsPolicy());
        executor.initialize();
        return executor;
    }
}