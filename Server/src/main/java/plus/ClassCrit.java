package plus;

import client.BuffStat;
import client.Character;
import client.Job;
import constants.skills.Bowmaster;
import tools.PacketCreator;
import tools.Pair;

import java.util.Collections;

/**
 * MapleStoryPlus: critical hits for every class.
 * <p>
 * In the original game only bowmen and assassins can crit, through their own skills. The client can show
 * critical hits for any class while it is under the Bowmaster's Sharp Eyes buff, so every other class is
 * given that effect permanently, with a chance and damage that grow at each job advancement.
 * <p>
 * The effect lives in the client only (the client works out damage). It is sent whenever a character
 * enters a map, which covers login, changing channel and respawning after death, and on job change.
 */
public class ClassCrit {
    // {critical chance in %, damage of a critical hit in %} for 1st, 2nd, 3rd and 4th job
    private static final int[][] TIERS = {{10, 150}, {15, 150}, {20, 160}, {25, 170}};

    public static void send(Character chr) {
        int[] tier = tierFor(chr.getJob());
        if (tier == null) {
            return;
        }
        // Sharp Eyes packs both numbers into one value: chance in the high byte, damage in the low byte.
        int value = tier[0] << 8 | tier[1];
        chr.sendPacket(PacketCreator.giveBuff(Bowmaster.SHARP_EYES, Integer.MAX_VALUE,
                Collections.singletonList(new Pair<>(BuffStat.SHARP_EYES, value))));
    }

    /** Whether this job crits through the effect sent here (used by the server's damage check). */
    public static boolean applies(Job job) {
        return tierFor(job) != null;
    }

    /** The crit tier for a job, or null when the job gets none here (beginners, and classes with their own crit). */
    static int[] tierFor(Job job) {
        if (hasOwnCrit(job)) {
            return null;
        }
        int id = job.getId();
        int branch = id % 1000;         // 1110 (Dawn Warrior 2nd job) and 110 (Fighter) share the same shape
        if (id / 100 == 22) {
            return null;                // Evan's job numbers do not follow the pattern
        }
        if (branch < 100) {
            return null;                // beginner, Noblesse, Legend
        }
        if (branch % 100 == 0) {
            return TIERS[0];
        }
        switch (branch % 10) {
            case 0:
                return TIERS[1];
            case 1:
                return TIERS[2];
            default:
                return TIERS[3];
        }
    }

    private static boolean hasOwnCrit(Job job) {
        return job.isA(Job.BOWMAN) || job.isA(Job.ASSASSIN) || job.isA(Job.WINDARCHER1) || job.isA(Job.NIGHTWALKER1);
    }
}
