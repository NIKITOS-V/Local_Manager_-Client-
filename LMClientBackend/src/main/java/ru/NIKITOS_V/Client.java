package ru.NIKITOS_V;

import ru.NIKITOS_V.Interfaces.ClientInterface;
import ru.NIKITOS_V.Interfaces.LogWriter;
import ru.NIKITOS_V.Logger.Logger;
import ru.NIKITOS_V.PyInterfaces.Recipient;
import ru.NIKITOS_V.RequestTypes.ClientRequestType;
import ru.NIKITOS_V.RequestTypes.ServerRequestType;

import java.io.*;
import java.net.Socket;
import java.nio.charset.StandardCharsets;

public class Client implements ClientInterface {
    private Recipient binder;

    private Socket socket;
    private BufferedReader bufferedReader;
    private BufferedWriter bufferedWriter;

    private final LogWriter logWriter;

    public Client(){
        this.logWriter = new Logger("Logs");

        this.logWriter.addLog(
                String.format(
                        "The %s class has been launched.",
                        this.getClass().getSimpleName()
                )
        );
    }

    public void setBinder(Recipient binder){
        this.binder = binder;
    }

    @Override
    public void setCSBinder(Recipient csBinder) {
        this.binder = csBinder;

        this.logWriter.addLog(
                String.format(
                        "The connecting class of the login window and the %s class has been received.",
                        this.getClass().getSimpleName()
                )
        );
    }

    @Override
    public void connect(String ip, int port, String userName) {
        new Thread(() -> {
            try{
                this.socket = new Socket(ip, port);

                this.bufferedWriter = new BufferedWriter(
                        new OutputStreamWriter(
                                socket.getOutputStream(),
                                StandardCharsets.UTF_8
                        )
                );

                this.bufferedReader = new BufferedReader(
                        new InputStreamReader(
                                socket.getInputStream(),
                                StandardCharsets.UTF_8
                        )
                );

                addTextToWriter(ClientRequestType.connect);
                addTextToWriter(userName);

                this.bufferedWriter.flush();

                this.logWriter.addLog("The user was connected.");

                startListeningThread();

                this.binder.accept_connection_result(true);

                this.logWriter.addLog("The chat window was open.");

            } catch (Exception e) {
                this.logWriter.addLog(e.toString());

                closeConnection();

                this.binder.accept_connection_result(false);
            }
        }).start();
    }

    @Override
    public void sendMessage(String message){
        if (this.bufferedWriter != null && !socket.isClosed()){
            try {
                addTextToWriter(ClientRequestType.sendMessage);

                String[] text = message.split("\n");

                addTextToWriter(text.length);

                for (String line: text){
                    addTextToWriter(line);
                }

                this.bufferedWriter.flush();

                this.logWriter.addLog("The message was sent.");

            } catch (Exception e) {
                this.logWriter.addLog(e.toString());

                closeConnection();
            }
        }
    }

    private void addTextToWriter(String text) throws IOException {
        this.bufferedWriter.write(text);
        this.bufferedWriter.newLine();
    }

    private void addTextToWriter(int number) throws IOException {
        addTextToWriter(String.valueOf(number));
    }

    private void addTextToWriter(ClientRequestType requestType) throws IOException {
        addTextToWriter(String.valueOf(requestType));
    }

    @Override
    public void getChatHistory(){
        if (this.bufferedWriter != null && !this.socket.isClosed()){
            try {
                addTextToWriter(ClientRequestType.getChatHistory);
                this.bufferedWriter.flush();

                this.logWriter.addLog("A request has been made for the chat history.");

            } catch (Exception e) {
                this.logWriter.addLog(e.toString());

                closeConnection();
            }
        }
    }

    @Override
    public void checkConnection(String ip, int port) {
        new Thread(() -> {
            try (Socket socket = new Socket(ip, port);
                 BufferedWriter bufferedWriter = new BufferedWriter(new OutputStreamWriter(socket.getOutputStream()))
            ){
                bufferedWriter.write(
                        String.valueOf(ClientRequestType.checkConnect)
                );
                bufferedWriter.newLine();
                bufferedWriter.flush();

                this.binder.accept_check_connection_result(true);

                this.logWriter.addLog("Connection verification was successful.");

            } catch (Exception e) {
                this.binder.accept_check_connection_result(false);

                this.logWriter.addLog(e.toString());
            }
        }).start();
    }

    private void startListeningThread(){
        new Thread(() -> {
            while (!this.socket.isClosed()) {
                try {
                    String requestType = this.bufferedReader.readLine();

                    if (!requestType.equals(String.valueOf(ServerRequestType.acceptMessage))) {
                         throw new IOException("Uncorrected request from server.");
                    }

                    StringBuilder message = new StringBuilder();

                    String userName = this.bufferedReader.readLine();

                    int numberLines = Integer.parseInt(this.bufferedReader.readLine());

                    for (int i = 0; i < numberLines; i++){
                        message.append(this.bufferedReader.readLine()).append("\n");
                    }

                    this.binder.accept_message(userName, message.toString());

                    this.logWriter.addLog("The message was received.");

                } catch (Exception e) {
                    this.logWriter.addLog(e.toString());

                    closeConnection();
                }
            }
        }).start();

        this.logWriter.addLog("The message acceptance thread has been started.");
    }

    public void closeConnection(){
        try {
            if (this.socket != null && !this.socket.isClosed() ){
                this.binder.log_out_of_chat();

                this.logWriter.addLog("The user returned to the login window.");

                this.socket.close();

                this.logWriter.addLog("The socket was closed.");

                if (this.bufferedWriter != null) {
                    this.bufferedWriter.close();

                    this.logWriter.addLog("The bufferedWriter was closed.");
                }

                if (this.bufferedReader != null) {
                    this.bufferedReader.close();

                    this.logWriter.addLog("The bufferedReader was closed.");
                }
            }
        } catch (Exception e) {
            this.logWriter.addLog(e.toString());
        }
    }
}
