package ru.NIKITOS_V.Interfaces;

import ru.NIKITOS_V.PyInterfaces.Recipient;

public interface ClientInterface {
    void connect(String ip, int port, String userName);

    void sendMessage(String message);

    void setCSBinder(Recipient csBinder);

    void getChatHistory();

    void checkConnection(String ip, int port);
}
