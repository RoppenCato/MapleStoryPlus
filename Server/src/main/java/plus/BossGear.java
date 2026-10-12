package plus;

import client.Character;
import client.inventory.Equip;
import client.inventory.Item;
import config.YamlConfig;
import org.slf4j.Logger;
import org.slf4j.LoggerFactory;
import server.ItemInformationProvider;
import server.life.Monster;

import java.io.File;
import java.nio.charset.StandardCharsets;
import java.nio.file.Files;
import java.util.ArrayList;
import java.util.List;
import java.util.concurrent.ThreadLocalRandom;

/**
 * MapleStoryPlus: every boss on the trials list drops two pieces of gear of its own level.
 * <p>
 * One is for the class of whoever killed it, down to the kind of weapon that job uses; the other is for
 * any class. Both come from the ordinary gear of the boss's level ({@code Boss-Gear.tsv} next to the
 * settings file, written by {@code Settings/Scripts/Make-Boss-Gear.py}), and both have better stats than
 * the same item from an ordinary monster: no stat rolls below the item's standard value.
 * <p>
 * The level is the boss's "gear level" in {@code Trials.tsv}: its own level, but never above what the
 * job it leads to needs.
 * <p>
 * Two tiers are boss loot only: level 110 (the Dragon weapons and the class sets of that level) from
 * Pianus, Bigfoot, Black Crow and Leviathan, and level 120 (Reverse and Timeless) from Papulatus, Zakum,
 * Horntail and Pink Bean. For those the roll is one weapon and one piece of armour, each for any class
 * and neither aimed at the killer: the gear is meant to be rare, and the roll is the fun of it.
 */
public class BossGear {
    private static final Logger log = LoggerFactory.getLogger(BossGear.class);
    private static final String[] CLASSES = {"warrior", "magician", "bowman", "thief", "pirate"};
    private static final int WINDOW = 5;            // gear needing a level within this of the boss's gear level
    private static final int WEAPON_ONE_IN = 4;     // one piece in four is a weapon, the rest armour
    private static final int RARE_TIER = 105;       // from this gear level up: a weapon and an armour for any class, none aimed

    private record Gear(int itemId, int level, String jobs, boolean weapon) {}

    private static List<Gear> gear;

    private static synchronized void load() {
        if (gear != null) {
            return;
        }
        gear = new ArrayList<>();
        File file = new File(new File(YamlConfig.CONFIG_FILE_NAME).getAbsoluteFile().getParentFile(), "Boss-Gear.tsv");
        try {
            List<String> lines = Files.readAllLines(file.toPath(), StandardCharsets.UTF_8);
            for (String line : lines.subList(1, lines.size())) {
                String[] cell = line.split("\t");
                if (cell.length >= 5) {
                    gear.add(new Gear(Integer.parseInt(cell[0]), Integer.parseInt(cell[2]), cell[3], cell[4].equals("weapon")));
                }
            }
        } catch (Exception e) {
            log.error("Boss-Gear.tsv could not be read", e);
        }
        log.info("Boss gear: {} items", gear.size());
    }

    /** The class of a job, or null for a beginner. Cygnus Knights, Aran and Evan count as their explorer class. */
    private static String classOf(int jobId) {
        if (jobId % 1000 < 100) {
            return null;
        }
        if (jobId / 100 == 21) {
            return "warrior";                       // Aran
        }
        if (jobId / 100 == 22) {
            return "magician";                      // Evan
        }
        int digit = jobId / 100 % 10;
        return digit >= 1 && digit <= 5 ? CLASSES[digit - 1] : null;
    }

    /** The kinds of weapon (item id / 10000) a job uses once it has chosen a branch; empty when any will do. */
    private static int[] weaponsOf(int jobId) {
        if (jobId >= 1000) {
            return new int[0];
        }
        return switch (jobId / 10) {
            case 11 -> new int[]{130, 131, 140, 141};       // Fighter line: swords and axes
            case 12 -> new int[]{130, 132, 140, 142};       // Page line: swords and blunt weapons
            case 13 -> new int[]{143, 144};                 // Spearman line
            case 31 -> new int[]{145};                      // bow
            case 32 -> new int[]{146};                      // crossbow
            case 41 -> new int[]{147};                      // claw
            case 42 -> new int[]{133};                      // dagger
            case 51 -> new int[]{148};                      // knuckler
            case 52 -> new int[]{149};                      // gun
            default -> new int[0];
        };
    }

    private static Gear pick(String cls, int[] weapons, int level) {
        return pick(cls, weapons, level, ThreadLocalRandom.current().nextInt(WEAPON_ONE_IN) == 0);
    }

    private static Gear pick(String cls, int[] weapons, int level, boolean wantWeapon) {
        ThreadLocalRandom r = ThreadLocalRandom.current();
        // Around the boss's level first; if the class has nothing there, reach further down
        for (int below = WINDOW; below <= 60; below += 5) {
            for (int attempt = 0; attempt < 2; attempt++) {
                boolean weapon = attempt == 0 ? wantWeapon : !wantWeapon;
                List<Gear> fits = new ArrayList<>();
                for (Gear g : gear) {
                    if (g.weapon() != weapon || g.level() < level - below || g.level() > level + WINDOW) {
                        continue;
                    }
                    if (cls != null && !("/" + g.jobs() + "/").contains("/" + cls + "/")) {
                        continue;
                    }
                    if (cls != null && weapon && weapons.length > 0) {
                        boolean mine = false;
                        for (int kind : weapons) {
                            mine |= g.itemId() / 10000 == kind;
                        }
                        if (!mine) {
                            continue;
                        }
                    }
                    fits.add(g);
                }
                if (!fits.isEmpty()) {
                    return fits.get(r.nextInt(fits.size()));
                }
            }
        }
        return null;
    }

    /** The item with stats rolled the usual way, except that none comes out below its standard value. */
    private static Item better(int itemId) {
        ItemInformationProvider ii = ItemInformationProvider.getInstance();
        Equip base = (Equip) ii.getEquipById(itemId);
        Equip rolled = ii.randomizeStats((Equip) ii.getEquipById(itemId));
        rolled.setStr(up(base.getStr(), rolled.getStr()));
        rolled.setDex(up(base.getDex(), rolled.getDex()));
        rolled.setInt(up(base.getInt(), rolled.getInt()));
        rolled.setLuk(up(base.getLuk(), rolled.getLuk()));
        rolled.setWatk(up(base.getWatk(), rolled.getWatk()));
        rolled.setMatk(up(base.getMatk(), rolled.getMatk()));
        rolled.setWdef(up(base.getWdef(), rolled.getWdef()));
        rolled.setMdef(up(base.getMdef(), rolled.getMdef()));
        rolled.setAcc(up(base.getAcc(), rolled.getAcc()));
        rolled.setAvoid(up(base.getAvoid(), rolled.getAvoid()));
        rolled.setSpeed(up(base.getSpeed(), rolled.getSpeed()));
        rolled.setJump(up(base.getJump(), rolled.getJump()));
        rolled.setHp(up(base.getHp(), rolled.getHp()));
        rolled.setMp(up(base.getMp(), rolled.getMp()));
        return rolled;
    }

    private static short up(short standard, short rolled) {
        return (short) (standard + Math.abs(rolled - standard));
    }

    /** What this boss drops on top of its own list: empty for a monster that is not on the trials list. */
    public static List<Item> roll(Character killer, Monster mob) {
        List<Item> drops = new ArrayList<>();
        int level = Trials.gearLevel(mob.getId());
        if (level <= 0) {
            return drops;
        }
        load();
        try {
            int job = killer.getJob().getId();
            String cls = classOf(job);
            if (cls == null) {
                cls = CLASSES[ThreadLocalRandom.current().nextInt(CLASSES.length)];
            }
            boolean rare = level >= RARE_TIER;
            Gear own = rare ? pick(null, new int[0], level, true) : pick(cls, weaponsOf(job), level);
            Gear any = rare ? pick(null, new int[0], level, false) : pick(null, new int[0], level);
            if (own != null) {
                drops.add(better(own.itemId()));
            }
            if (any != null) {
                drops.add(better(any.itemId()));
            }
        } catch (Exception e) {
            log.error("Boss gear for {} could not be rolled", mob.getName(), e);
        }
        return drops;
    }
}
