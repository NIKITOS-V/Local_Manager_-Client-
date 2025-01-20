package Logger;

import Interfaces.LogWriter;

import java.io.File;
import java.io.FileWriter;
import java.text.SimpleDateFormat;
import java.util.Calendar;


public class Logger implements LogWriter {
    public static final String FILE_EXTENSION = "txt";
    public static final String PATTERN = "yyyy.MM.dd";

    private final String logsDir;

    public Logger(String logsDir){
        this.logsDir = logsDir;

        addLog("", false, "");
    }

    @Override
    public void addLog(String text) {
        addLog(text, true, "\n");
    }

    private void addLog(String text, boolean append, String end){
        try {
            File file = new File(createFilePath());

            file.createNewFile();

            FileWriter fileWriter = new FileWriter(file, append);

            fileWriter.write(text);
            fileWriter.append(end);
            fileWriter.flush();

            fileWriter.close();

        } catch (Exception e) {
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
