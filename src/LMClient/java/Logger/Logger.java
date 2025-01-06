package Logger;

import java.io.File;
import java.io.FileWriter;
import java.io.IOException;
import java.text.SimpleDateFormat;
import java.util.Calendar;


public class Logger implements LogWriter{
    private static final String FILE_EXTENSION = "txt";
    private static final String PATTERN = "yyyy.MM.dd";

    private final String logsDir;

    public Logger(String logsDir){
        this.logsDir = logsDir;
    }

    @Override
    public void addLog(String text) {
        try {
            File file = new File(createFilePath());

            file.createNewFile();

            FileWriter fileWriter = new FileWriter(file, true);

            fileWriter.write(text);
            fileWriter.append("\n");
            fileWriter.flush();

            fileWriter.close();

        } catch (IOException e) {
            e.printStackTrace();
        }
    }

    private String createFilePath(){
        return String.format(
                "%s/%s.%s",
                this.logsDir,
                createFileName(),
                FILE_EXTENSION
        );
    }

    private String createFileName(){
        return new SimpleDateFormat(PATTERN).format(Calendar.getInstance().getTime());
    }
}
