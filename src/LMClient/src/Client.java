import Interfaces.ClientInterface;
import Interfaces.RecipientConnectionResult;
import Interfaces.RecipientMessages;
import RequestTypes.ClientRequestType;
import RequestTypes.ServerRequestType;

import java.io.*;
import java.net.Socket;
import java.nio.charset.StandardCharsets;

public class Client implements ClientInterface {
    private RecipientMessages csBinder;
    private RecipientConnectionResult esBinder;

    private Socket socket;
    private BufferedReader bufferedReader;
    private BufferedWriter bufferedWriter;

    @Override
    public void setCSBinder(RecipientMessages csBinder) {
        this.csBinder = csBinder;
    }

    @Override
    public void setESBinder(RecipientConnectionResult esBinder) {
        this.esBinder = esBinder;
    }

    @Override
    public void connect(String ip, Integer port, String userName) {
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

                startListeningThread();

                this.esBinder.accept_connection_result(true);

            } catch (IOException e) {
                closeConnection();

                this.esBinder.accept_connection_result(false);
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

            } catch (IOException e) {
               closeConnection();
            }
        }
    }

    private void addTextToWriter(String text) throws IOException {
        this.bufferedWriter.write(text);
        this.bufferedWriter.newLine();
    }

    private void addTextToWriter(Integer number) throws IOException {
        addTextToWriter(String.valueOf(number));
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

            } catch (IOException e) {
               closeConnection();
            }
        }
    }

    @Override
    public void checkConnection(String ip, Integer port) {
        new Thread(() -> {
            try (Socket socket = new Socket(ip, port);
                 BufferedWriter bufferedWriter = new BufferedWriter(new OutputStreamWriter(socket.getOutputStream()))
            ){
                bufferedWriter.write(
                        String.valueOf(ClientRequestType.checkConnect)
                );
                bufferedWriter.newLine();
                bufferedWriter.flush();

                this.esBinder.accept_check_connection_result(true);

            } catch (IOException e) {

                this.esBinder.accept_check_connection_result(false);
            }
        }).start();
    }

    private void startListeningThread(){
        new Thread(() -> {
            while (!this.socket.isClosed()) {
                try {
                    String requestType = this.bufferedReader.readLine();

                    if (!requestType.equals(String.valueOf(ServerRequestType.acceptMessage))) {
                         throw new IOException("Uncorrected request from server");
                    }

                    StringBuilder message = new StringBuilder();

                    String userName = this.bufferedReader.readLine();

                    Integer numberLines = Integer.parseInt(this.bufferedReader.readLine());

                    for (int i = 0; i < numberLines; i++){
                        message.append(this.bufferedReader.readLine()).append("\n");
                    }

                    this.csBinder.accept_message(userName, message.toString());

                } catch (IOException e) {
                    closeConnection();
                }
            }
        }).start();
    }

    public void closeConnection(){
        try {
            System.out.println("sterllll");

            this.csBinder.log_out_of_chat();

            if (this.socket != null){

                this.socket.close();
            }

            if (this.bufferedWriter != null) {

                this.bufferedWriter.close();
            }

            if (this.bufferedReader != null) {

                this.bufferedReader.close();
            }

            System.out.println("succj");

        } catch (IOException e) {
            e.printStackTrace();
        }
    }
}
