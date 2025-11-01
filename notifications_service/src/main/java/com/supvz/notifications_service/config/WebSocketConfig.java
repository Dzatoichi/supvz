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
    @Value("${websocket.allowed_origins}")
    private String[] origins;

    /**
     * Настройка ручки, по которой можно подключить клиента с сервером.
     * Также указывается Allowed-Origin для подключения только доверенных клиентов.
     */
    @Override
    public void registerStompEndpoints(StompEndpointRegistry registry) {
        registry.addEndpoint("/ws")
//                todo: поменять обязательно для прода
                .setAllowedOriginPatterns("*")
                .withSockJS();
    }

    /**
     * Конфигурация логики роутинга сообщений уже внутри STOMP соединения.
     */
    @Override
    public void configureMessageBroker(MessageBrokerRegistry registry) {
        registry.enableSimpleBroker("/topic");

        registry.setApplicationDestinationPrefixes("/backend");
    }
}
