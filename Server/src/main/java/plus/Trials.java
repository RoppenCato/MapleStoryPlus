package plus;

import client.Character;
import client.Job;
import client.Skill;
import client.SkillFactory;
import config.YamlConfig;
import constants.game.GameConstants;
import net.server.world.PartyCharacter;
import org.slf4j.Logger;
import org.slf4j.LoggerFactory;
import server.life.Monster;
import soloMapling.ArtificialPlayer.BotHelpers;
import tools.DatabaseConnection;

import java.io.File;
import java.nio.charset.StandardCharsets;
import java.nio.file.Files;
import java.sql.Connection;
import java.sql.PreparedStatement;
import java.sql.ResultSet;
import java.sql.Statement;
import java.util.ArrayList;
import java.util.HashSet;
import java.util.LinkedHashMap;
import java.util.List;
import java.util.Map;
import java.util.Set;

/**
 * MapleStoryPlus: job advancement through trials, and the Guide that shows it (the Trade button).
 * <p>
 * An explorer advances by reaching the level and beating bosses, not through the original quests:
 * <ul>
 * <li>1st job at level 10 (8 for a magician): choose a class.</li>
 * <li>2nd job at 30: both bosses of band 1.</li>
 * <li>3rd job at 70: any 4 bosses of band 2.</li>
 * <li>4th job at 120: any 4 bosses of band 3.</li>
 * </ul>
 * The bosses are listed in {@code Trials.tsv} next to the settings file. Every kill of one is recorded per
 * character in the table {@code plus_trials}. The texts of the Guide are built here so that the script
 * ({@code scripts/npc/plusGuide.js}) only has to show them.
 */
public class Trials {
    private static final Logger log = LoggerFactory.getLogger(Trials.class);

    private record Boss(int band, int mobId, String name, String where) {}

    /** Per band: the level of the job it opens, and how many of its bosses must be beaten. */
    private static final int[][] BANDS = {{}, {30, 2}, {70, 4}, {120, 4}};
    private static final String[] TIER_NAMES = {"", "1st", "2nd", "3rd", "4th"};
    private static final int[] INSTRUCTORS = {
            1022000, 1032001, 1012100, 1052001, 1090000,        // 1st and 2nd job
            2020008, 2020009, 2020010, 2020011, 2020013,        // 3rd job
            2081100, 2081200, 2081300, 2081400, 2081500};       // 4th job
    /** On reaching 4th job these are opened to level 10 at once; every other 4th job skill waits for tokens. */
    private static final Map<Integer, int[]> FOURTH_JOB_BASICS = Map.ofEntries(
            Map.entry(112, new int[]{1121008, 1121000}), Map.entry(122, new int[]{1221009, 1221000}),
            Map.entry(132, new int[]{1320006, 1321000}), Map.entry(212, new int[]{2121006, 2121000}),
            Map.entry(222, new int[]{2221006, 2221000}), Map.entry(232, new int[]{2321007, 2321000}),
            Map.entry(312, new int[]{3121004, 3121000}), Map.entry(322, new int[]{3221001, 3221000}),
            Map.entry(412, new int[]{4121007, 4121000}), Map.entry(422, new int[]{4221007, 4221000}),
            Map.entry(512, new int[]{5121007, 5121000}), Map.entry(522, new int[]{5221004, 5221000}));

    private static List<Boss> bosses;
    private static Map<Integer, Boss> byMob;

    private static synchronized void load() {
        if (bosses != null) {
            return;
        }
        bosses = new ArrayList<>();
        byMob = new LinkedHashMap<>();
        File file = new File(new File(YamlConfig.CONFIG_FILE_NAME).getAbsoluteFile().getParentFile(), "Trials.tsv");
        try {
            List<String> lines = Files.readAllLines(file.toPath(), StandardCharsets.UTF_8);
            for (String line : lines.subList(1, lines.size())) {
                String[] cell = line.split("\t");
                if (cell.length >= 3) {
                    Boss boss = new Boss(Integer.parseInt(cell[0]), Integer.parseInt(cell[1]), cell[2], cell.length > 3 ? cell[3] : "");
                    bosses.add(boss);
                    byMob.put(boss.mobId(), boss);
                }
            }
        } catch (Exception e) {
            log.error("Trials.tsv could not be read", e);
        }
        try (Connection con = DatabaseConnection.getConnection(); Statement st = con.createStatement()) {
            st.execute("CREATE TABLE IF NOT EXISTS plus_trials (characterid INT NOT NULL, mobid INT NOT NULL, "
                    + "kills INT NOT NULL DEFAULT 0, first_kill DATETIME NOT NULL, PRIMARY KEY (characterid, mobid))");
        } catch (Exception e) {
            log.error("The trials table could not be created", e);
        }
        log.info("Trials: {} bosses in {} bands", bosses.size(), BANDS.length - 1);
    }

    public static boolean isInstructor(int npcId) {
        for (int id : INSTRUCTORS) {
            if (id == npcId) {
                return true;
            }
        }
        return false;
    }

    // ------------------------------------------------------------------------------------------
    // Jobs
    // ------------------------------------------------------------------------------------------

    private static boolean isExplorer(Job job) {
        return job.getId() < 600;
    }

    /** 0 for a beginner, 1 to 4 for the job advancements. */
    private static int tier(Job job) {
        int id = job.getId();
        return id == 0 ? 0 : id % 100 == 0 ? 1 : id % 10 == 0 ? 2 : id % 10 == 1 ? 3 : 4;
    }

    private static int levelFor(int tier) {
        return tier == 1 ? 10 : BANDS[tier - 1][0];
    }

    /** The jobs this character could advance to next, whether or not it is ready. */
    private static List<Integer> nextJobs(Job job) {
        List<Integer> next = new ArrayList<>();
        int id = job.getId();
        switch (tier(job)) {
            case 0 -> { next.add(100); next.add(200); next.add(300); next.add(400); next.add(500); }
            case 1 -> {
                next.add(id + 10);
                next.add(id + 20);
                if (id == 100 || id == 200) {
                    next.add(id + 30);
                }
            }
            case 2, 3 -> next.add(id + 1);
            default -> { }
        }
        return next;
    }

    // ------------------------------------------------------------------------------------------
    // Kills
    // ------------------------------------------------------------------------------------------

    private static Set<Integer> beaten(Character chr) {
        Set<Integer> done = new HashSet<>();
        try (Connection con = DatabaseConnection.getConnection();
             PreparedStatement ps = con.prepareStatement("SELECT mobid FROM plus_trials WHERE characterid = ?")) {
            ps.setInt(1, chr.getId());
            try (ResultSet rs = ps.executeQuery()) {
                while (rs.next()) {
                    done.add(rs.getInt(1));
                }
            }
        } catch (Exception e) {
            log.error("Could not read the trials of {}", chr.getName(), e);
        }
        return done;
    }

    private static int beatenInBand(Set<Integer> done, int band) {
        int count = 0;
        for (Boss boss : bosses) {
            if (boss.band() == band && done.contains(boss.mobId())) {
                count++;
            }
        }
        return count;
    }

    /** Called when a monster dies. The killer and the party members on the same map get the credit. */
    public static void onKill(Character killer, Monster monster) {
        load();
        Boss boss = byMob.get(monster.getId());
        if (boss == null || killer == null) {
            return;
        }
        List<Character> credited = new ArrayList<>();
        credited.add(killer);
        if (killer.getParty() != null) {
            for (PartyCharacter member : killer.getParty().getMembers()) {
                Character other = killer.getMap().getCharacterById(member.getId());
                if (other != null && other != killer) {
                    credited.add(other);
                }
            }
        }
        for (Character chr : credited) {
            if (BotHelpers.isBot(chr)) {
                continue;
            }
            boolean first = !beaten(chr).contains(boss.mobId());
            try (Connection con = DatabaseConnection.getConnection();
                 PreparedStatement ps = con.prepareStatement("INSERT INTO plus_trials (characterid, mobid, kills, first_kill) "
                         + "VALUES (?, ?, 1, NOW()) ON DUPLICATE KEY UPDATE kills = kills + 1")) {
                ps.setInt(1, chr.getId());
                ps.setInt(2, boss.mobId());
                ps.executeUpdate();
            } catch (Exception e) {
                log.error("Could not record the trial {} for {}", boss.name(), chr.getName(), e);
                continue;
            }
            if (first) {
                int done = beatenInBand(beaten(chr), boss.band());
                int needed = BANDS[boss.band()][1];
                String job = TIER_NAMES[boss.band() + 1] + " job";
                if (done < needed) {
                    chr.dropMessage(5, "Trial beaten: " + boss.name() + ". " + done + " of " + needed + " for " + job + ".");
                } else if (done == needed) {
                    chr.dropMessage(5, "Trial beaten: " + boss.name() + ". That is all " + needed + " for " + job
                            + "! Press the Trade button to open the Guide" + (chr.getLevel() >= BANDS[boss.band()][0] ? "." : " once you are level " + BANDS[boss.band()][0] + "."));
                } else {
                    chr.dropMessage(5, "Trial beaten: " + boss.name() + ".");
                }
            }
        }
    }

    // ------------------------------------------------------------------------------------------
    // The Guide
    // ------------------------------------------------------------------------------------------

    /** Why this character cannot advance yet; empty when it can. */
    private static String blocker(Character chr, Set<Integer> done) {
        Job job = chr.getJob();
        int next = tier(job) + 1;
        if (!isExplorer(job)) {
            return "The trials are for explorers. Your class advances the way it always has.";
        }
        if (next > 4) {
            return "You have reached 4th job. There is no advancement left.";
        }
        if (chr.getLevel() < (next == 1 ? 8 : levelFor(next))) {
            return "You need level " + levelFor(next) + (next == 1 ? " (8 for a magician)" : "") + " for " + TIER_NAMES[next] + " job. You are level " + chr.getLevel() + ".";
        }
        if (next >= 2) {
            int have = beatenInBand(done, next - 1);
            if (have < BANDS[next - 1][1]) {
                return "You have beaten " + have + " of the " + BANDS[next - 1][1] + " trials needed for " + TIER_NAMES[next] + " job.";
            }
        }
        return "";
    }

    /** The first page: where you stand and what you can do. */
    public static String menu(Character chr) {
        load();
        Set<Integer> done = beaten(chr);
        String why = blocker(chr, done);
        StringBuilder text = new StringBuilder("#e" + chr.getName() + "#n, level " + chr.getLevel() + " " + GameConstants.getJobName(chr.getJob().getId()) + ".\r\n");
        text.append(why.isEmpty() ? "#bYou are ready to advance.#k" : why).append("\r\n#b");
        text.append("\r\n#L0#My job advancement#l");
        text.append("\r\n#L1#Trials: the bosses to beat#l");
        text.append("\r\n#L2#4th job skills#l");
        return text.toString();
    }

    /** The job page: either why not yet, or the jobs to choose from as a selection list (#L<job id>#). */
    public static String jobPage(Character chr) {
        load();
        Set<Integer> done = beaten(chr);
        String why = blocker(chr, done);
        Job job = chr.getJob();
        if (!why.isEmpty()) {
            StringBuilder text = new StringBuilder(why);
            int next = tier(job) + 1;
            if (isExplorer(job) && next >= 2 && next <= 4) {
                text.append("\r\n\r\n").append(TIER_NAMES[next]).append(" job needs level ").append(levelFor(next)).append(" and ")
                        .append(BANDS[next - 1][1] == bandSize(next - 1) ? "all " : "any ").append(BANDS[next - 1][1])
                        .append(" of the ").append(bandSize(next - 1)).append(" trials of that band.");
            }
            return text.toString();
        }
        StringBuilder text = new StringBuilder("You are ready for #e" + TIER_NAMES[tier(job) + 1] + " job#n. This cannot be undone.\r\n#b");
        for (int id : nextJobs(job)) {
            if (id == 200 || chr.getLevel() >= 10) {        // only a magician can start at level 8
                text.append("\r\n#L").append(id).append("#Become a ").append(GameConstants.getJobName(id)).append("#l");
            }
        }
        return text.toString();
    }

    public static boolean canAdvance(Character chr) {
        load();
        return blocker(chr, beaten(chr)).isEmpty();
    }

    /** Advances the character to the chosen job if that is allowed. Returns what to tell the player. */
    public static String advance(Character chr, int jobId) {
        load();
        Job job = chr.getJob();
        if (!blocker(chr, beaten(chr)).isEmpty() || !nextJobs(job).contains(jobId) || (jobId != 200 && chr.getLevel() < 10)) {
            return "You cannot advance to that job now.";
        }
        Job target = Job.getById(jobId);
        if (target == null) {
            return "That job does not exist.";
        }
        chr.changeJob(target);
        StringBuilder told = new StringBuilder("You are now a #e" + GameConstants.getJobName(jobId) + "#n.");
        int[] basics = FOURTH_JOB_BASICS.get(jobId);
        if (basics != null) {
            for (int skillId : basics) {
                Skill skill = SkillFactory.getSkill(skillId);
                if (skill != null && chr.getMasterLevel(skill) < 10) {
                    chr.changeSkillLevel(skill, chr.getSkillLevel(skill), 10, -1);
                }
            }
            told.append("\r\nYour main attack and Maple Warrior are open to level 10. The other 4th job skills are earned with boss tokens.");
        }
        log.info("{} advanced to {} through the Guide", chr.getName(), target);
        return told.toString();
    }

    private static int bandSize(int band) {
        int size = 0;
        for (Boss boss : bosses) {
            if (boss.band() == band) {
                size++;
            }
        }
        return size;
    }

    /** The trials page: every band with what is beaten and what is left. */
    public static String trialsPage(Character chr) {
        load();
        Set<Integer> done = beaten(chr);
        int current = Math.max(1, Math.min(3, tier(chr.getJob())));
        StringBuilder text = new StringBuilder();
        for (int band = 1; band <= 3; band++) {
            int needed = BANDS[band][1];
            int have = beatenInBand(done, band);
            text.append("#e").append(TIER_NAMES[band + 1]).append(" job#n (level ").append(BANDS[band][0]).append("): ")
                    .append(Math.min(have, needed)).append(" of ").append(needed).append(have >= needed ? "  #gdone#k" : "").append("\r\n");
            if (band != current && !(band < current && have < needed)) {
                continue;                                   // only the band you are working on is listed in full
            }
            for (Boss boss : bosses) {
                if (boss.band() == band) {
                    text.append(done.contains(boss.mobId()) ? "  #g[x]#k " : "  [ ] ").append(boss.name())
                            .append(done.contains(boss.mobId()) ? "" : "#d, " + boss.where() + "#k").append("\r\n");
                }
            }
        }
        return text.toString();
    }

    /** The trials as plain chat lines, for the @goals command. */
    public static List<String> goals(Character chr) {
        load();
        Set<Integer> done = beaten(chr);
        List<String> lines = new ArrayList<>();
        String why = blocker(chr, done);
        lines.add(why.isEmpty() ? "You are ready to advance. Press the Trade button to open the Guide." : why);
        int band = tier(chr.getJob());
        if (isExplorer(chr.getJob()) && band >= 1 && band <= 3) {
            StringBuilder left = new StringBuilder();
            for (Boss boss : bosses) {
                if (boss.band() == band && !done.contains(boss.mobId())) {
                    left.append(left.length() > 0 ? ", " : "").append(boss.name());
                }
            }
            if (beatenInBand(done, band) < BANDS[band][1] && left.length() > 0) {
                lines.add("Still to beat (any " + (BANDS[band][1] - beatenInBand(done, band)) + "): " + left);
            }
        }
        return lines;
    }

    public static String fourthJobPage(Character chr) {
        if (tier(chr.getJob()) < 4) {
            return "This is for 4th job. On advancing you get your main attack and Maple Warrior at once; the other skills are earned with tokens from bosses.";
        }
        return "Your main attack and Maple Warrior are open to level 10.\r\n\r\nThe token shop for the other 4th job skills is not built yet.";
    }
}
