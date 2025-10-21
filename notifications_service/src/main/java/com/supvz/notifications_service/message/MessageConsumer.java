package com.supvz.notifications_service.message;

public interface MessageConsumer {
    void consume(String message);
}
