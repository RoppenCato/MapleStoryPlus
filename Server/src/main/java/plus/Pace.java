package plus;

import client.Character;
import config.YamlConfig;
import org.slf4j.Logger;
import org.slf4j.LoggerFactory;

import java.io.File;
import java.nio.charset.StandardCharsets;
import java.nio.file.Files;
import java.util.List;
import java.util.TreeMap;

/**
 * MapleStoryPlus: how fast a character levels depends on its level.
 * <p>
 * One exp rate for the whole game makes the first 30 levels fly and levels 31 to 80 a wall of 2,000 to
 * 2,600 kills each. So on top of the world's rates there is a pace: a multiplier that depends only on
 * the level of the player ({@code Pace.tsv} next to the settings file). It never looks at the monster,
 * so a player may stay on monsters they have outlevelled; those just give their own, smaller exp.
 * <p>
 * The pace multiplies three things a kill gives: exp, the mesos dropped and the chance of each item
 * (not from bosses, which are not killed more or less often because of it). That way a level still
 * gives the same mesos, gear and other drops as before; it only takes fewer kills.
 */
public class Pace {
    private static final Logger log = LoggerFactory.getLogger(Pace.class);
    private static TreeMap<Integer, Double> steps;

    private static synchronized void load() {
        if (steps != null) {
            return;
        }
        steps = new TreeMap<>();
        File file = new File(new File(YamlConfig.CONFIG_FILE_NAME).getAbsoluteFile().getParentFile(), "Pace.tsv");
        try {
            List<String> lines = Files.readAllLines(file.toPath(), StandardCharsets.UTF_8);
            for (String line : lines.subList(1, lines.size())) {
                String[] cell = line.split("\t");
                if (cell.length >= 2) {
                    steps.put(Integer.parseInt(cell[0].trim()), Double.parseDouble(cell[1].trim()));
                }
            }
        } catch (Exception e) {
            log.error("Pace.tsv could not be read; the pace is 1 at every level", e);
        }
    }

    /** The multiplier at this level: the row of Pace.tsv with the highest from_level not above it. */
    public static double at(int level) {
        load();
        var step = steps.floorEntry(level);
        return step == null ? 1.0 : step.getValue();
    }

    public static double of(Character chr) {
        return chr == null ? 1.0 : at(chr.getLevel());
    }
}
