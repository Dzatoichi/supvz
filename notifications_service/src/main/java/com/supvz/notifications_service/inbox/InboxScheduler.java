package com.supvz.notifications_service.inbox;

public interface InboxScheduler {
    void pollForProcessing();

    void pollForCleaning();
}
