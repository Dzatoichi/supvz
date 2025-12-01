package com.supvz.notifications_service.config;

import org.springframework.beans.factory.annotation.Value;
import org.springframework.context.annotation.Configuration;
import org.springframework.messaging.simp.config.MessageBrokerRegistry;
import org.springframework.web.socket.config.annotation.EnableWebSocketMessageBroker;
import org.springframework.web.socket.config.annotation.StompEndpointRegistry;
import org.springframework.web.socket.config.annotation.WebSocketMessageBrokerConfigurer;


/**
 * <h3>
 * Веб-сокет конфигурация для real-time уведомлений (типа web).
 * </h3>
 * Конфигурация включает поддержку Веб-сокета с протоколом STOMP для отправления real-time уведомлений подключенным клиентам.
 */
@Configuration
@EnableWebSocketMessageBroker
public class WebSocketConfig implements WebSocketMessageBrokerConfigurer {
    @Value("${app.websocket.allowed-origins}")
    private String[] origins;
    @Value("{app.websocket.base-topic}")
    private String baseTopic;

    /**
     * Настройка ручки, по которой можно подключить клиента с сервером.
     * Также указывается Allowed-Origin для подключения только доверенных клиентов.
     */
    @Override
    public void registerStompEndpoints(StompEndpointRegistry registry) {
        registry.addEndpoint("/ws")
                .setAllowedOriginPatterns(origins)
                .withSockJS();
    }

    /**
     * Конфигурация логики роутинга сообщений уже внутри STOMP соединения.
     */
    @Override
    public void configureMessageBroker(MessageBrokerRegistry registry) {
        registry.enableSimpleBroker(baseTopic);
        registry.setApplicationDestinationPrefixes("/backend");
    }
}