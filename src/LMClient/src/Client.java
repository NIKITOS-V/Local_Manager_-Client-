import Interfases.Recipient;

import java.io.*;
import java.net.Socket;
import java.net.UnknownHostException;

public class Client {
    private Recipient csBinder;
    private int userID;

    BufferedReader bufferedReader;
    BufferedWriter bufferedWriter;

    public void setCSBinder(Recipient csBinder) {
        this.csBinder = csBinder;
    }

    public void connect(String ip, Integer port, String userName){

    }

    public static boolean checkConnection(String ip, Integer port) {
        try (Socket socket = new Socket(ip, port)) {

        } catch (IOException e) {
            return false;
        }

        return true;
    }

    public void sendMessage(String message){
        if (bufferedWriter != null){
            try {
                bufferedWriter.write(createRequest(message));
            } catch (IOException e) {
               closeBuffers();
            }
        }
    }

    private void startRecipientThread(String ip, Integer port){

    }

    private String createRequest(String message){
        return String.format(
                "%s %s %s",
                RequestType.message,
                this.userID,
                message
        );
    }

    private void closeBuffers(){
        try {
            this.bufferedWriter.close();
            this.bufferedReader.close();
        } catch (IOException e) {
            throw new RuntimeException(e);
        }
    }
}
