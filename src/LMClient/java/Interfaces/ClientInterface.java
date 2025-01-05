package Interfaces;

public interface ClientInterface {
    void connect(String ip, Integer port, String userName);

    void sendMessage(String message);

    void setCSBinder(RecipientMessages csBinder);

    void setESBinder(RecipientConnectionResult esBinder);

    void getChatHistory();

    void checkConnection(String ip, Integer port);
}
