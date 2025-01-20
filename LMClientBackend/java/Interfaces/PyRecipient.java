package Interfaces;

public interface PyRecipient {
    void accept_message(String user_name, String message);
    void log_out_of_chat();
    void accept_check_connection_result(boolean result);
    void accept_connection_result(boolean result);
}
