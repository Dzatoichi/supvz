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

@Configuration
@EnableScheduling
@EnableRetry
@EnableAsync
public class AppConfig {
    @Value("${app.notification.thread.core-pool-size:20}")
    private Integer notificationCorePoolSize;
    @Value("${app.notification.thread.max-pool-size:50}")
    private Integer notificationMaxPoolSize;
    @Value("${app.notification.thread.queue-capacity:50}")
    private Integer notificationQueueCapacity;
    @Value("${app.notification.thread.name-prefix:notification}")
    private String notificationThreadNamePrefix;
    @Value("${app.notification.thread.wait-tasks-shutdown:true}")
    private Boolean notificationWaitTasksShutdown;
    @Value("${app.notification.await-termination-sec:60}")
    private Integer notificationAwaitTerminationSeconds;


    @Bean
    public ObjectMapper objectMapper() {
        return new ObjectMapper()
                .enable(READ_UNKNOWN_ENUM_VALUES_AS_NULL)
                .registerModule(new JavaTimeModule());
    }

    @Bean
    public Executor notificationExecutor() {
        ThreadPoolTaskExecutor executor = new ThreadPoolTaskExecutor();
        executor.setCorePoolSize(notificationCorePoolSize);
        executor.setMaxPoolSize(notificationMaxPoolSize);
        executor.setQueueCapacity(notificationQueueCapacity);
        executor.setThreadNamePrefix(notificationThreadNamePrefix);
        executor.setWaitForTasksToCompleteOnShutdown(notificationWaitTasksShutdown);
        executor.setAwaitTerminationSeconds(notificationAwaitTerminationSeconds);
        executor.setRejectedExecutionHandler(new ThreadPoolExecutor.CallerRunsPolicy());
        executor.initialize();
        return executor;
    }
}