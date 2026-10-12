package plus;

import client.keybind.KeyBinding;
import client.keybind.QuickslotBinding;
import config.YamlConfig;
import constants.game.GameConstants;
import org.slf4j.Logger;
import org.slf4j.LoggerFactory;

import java.io.File;
import java.nio.charset.StandardCharsets;
import java.nio.file.Files;
import java.sql.Connection;
import java.sql.PreparedStatement;
import java.util.LinkedHashMap;
import java.util.Map;

/**
 * MapleStoryPlus: the key bindings a new character starts with.
 * <p>
 * They come from {@code Default-Keys.tsv} next to the settings file, which
 * {@code Settings/Scripts/Save-Default-Keys.py} writes from a character that is set up the way the
 * player likes. Without the file a new character gets the game's own default keys. The file is read
 * again for every new character, so a new copy takes effect without a restart.
 * <p>
 * The eight quick slots are kept per account, so a new account gets the saved ones with its first
 * character; an account that already has its own keeps them.
 */
public class DefaultKeys {
    private static final Logger log = LoggerFactory.getLogger(DefaultKeys.class);

    private record Saved(Map<Integer, KeyBinding> keys, byte[] quickslots) {}

    private static Saved read() {
        Map<Integer, KeyBinding> keys = new LinkedHashMap<>();
        byte[] quickslots = null;
        File file = new File(new File(YamlConfig.CONFIG_FILE_NAME).getAbsoluteFile().getParentFile(), "Default-Keys.tsv");
        if (file.exists()) {
            try {
                for (String line : Files.readAllLines(file.toPath(), StandardCharsets.UTF_8)) {
                    String[] cell = line.split("\t");
                    if (cell.length >= 9 && cell[0].equals("quickslots")) {
                        quickslots = new byte[QuickslotBinding.QUICKSLOT_SIZE];
                        for (int i = 0; i < quickslots.length; i++) {
                            quickslots[i] = (byte) Integer.parseInt(cell[i + 1].trim());
                        }
                    } else if (cell.length >= 3 && cell[0].matches("\\d+")) {
                        keys.put(Integer.parseInt(cell[0]), new KeyBinding(Integer.parseInt(cell[1].trim()), Integer.parseInt(cell[2].trim())));
                    }
                }
            } catch (Exception e) {
                log.error("Default-Keys.tsv could not be read; new characters get the game's default keys", e);
                keys.clear();
                quickslots = null;
            }
        }
        if (keys.isEmpty()) {
            int[] key = GameConstants.getCustomKey(YamlConfig.config.server.USE_CUSTOM_KEYSET);
            int[] type = GameConstants.getCustomType(YamlConfig.config.server.USE_CUSTOM_KEYSET);
            int[] action = GameConstants.getCustomAction(YamlConfig.config.server.USE_CUSTOM_KEYSET);
            for (int i = 0; i < key.length; i++) {
                keys.put(key[i], new KeyBinding(type[i], action[i]));
            }
        }
        return new Saved(keys, quickslots);
    }

    /** Key number to what it does, for a new character. */
    public static Map<Integer, KeyBinding> keys() {
        return read().keys();
    }

    /** Gives the account the saved quick slots, unless it already has quick slots of its own. */
    public static void giveQuickslots(Connection con, int accountId) {
        byte[] quickslots = read().quickslots();
        if (quickslots == null) {
            return;
        }
        try (PreparedStatement ps = con.prepareStatement("INSERT IGNORE INTO quickslotkeymapped (accountid, keymap) VALUES (?, ?)")) {
            ps.setInt(1, accountId);
            ps.setLong(2, tools.LongTool.BytesToLong(quickslots));
            ps.executeUpdate();
        } catch (Exception e) {
            log.error("Could not give account {} the saved quick slots", accountId, e);
        }
    }
}
