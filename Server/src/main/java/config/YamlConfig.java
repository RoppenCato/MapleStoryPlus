package config;

import com.esotericsoftware.yamlbeans.YamlReader;
import constants.string.CharsetConstants;

import java.io.FileNotFoundException;
import java.io.IOException;
import java.nio.file.Files;
import java.nio.file.Path;
import java.util.List;


public class YamlConfig {
    // Either provide a custom config file path through the "config-path" property when launching the .jar, or don't provide one to use the default "config.yaml"
    public static final String CONFIG_FILE_NAME = System.getProperty("config-path", "config.yaml");
    public static final YamlConfig config = loadConfig();

    public List<WorldConfig> worlds;
    public ServerConfig server;

    private static YamlConfig loadConfig() {
        try {
            YamlReader reader = new YamlReader(Files.newBufferedReader(Path.of(CONFIG_FILE_NAME), CharsetConstants.CHARSET));
            YamlConfig config = reader.read(YamlConfig.class);
            reader.close();
            return config;
        } catch (FileNotFoundException e) {
            throw new RuntimeException("Could not read config file " + YamlConfig.CONFIG_FILE_NAME + ": " + e.getMessage());
        } catch (IOException e) {
            throw new RuntimeException("Could not successfully parse config file " + YamlConfig.CONFIG_FILE_NAME + ": " + e.getMessage());
        }
    }
}
