package plus;

import server.life.MonsterDropEntry;

import java.util.List;
import java.util.concurrent.ThreadLocalRandom;

/**
 * MapleStoryPlus: a boss never drops nothing.
 * <p>
 * Every drop of a monster is rolled on its own, so a boss with a short or stingy list can leave only mesos
 * behind. When that happens, one item from its list is dropped anyway. Likelier items are picked more
 * often, in proportion to their chance, so the rare ones stay rare.
 */
public class BossDrops {
    /** One item from the boss's ordinary drops, or null if its list has no items. */
    public static MonsterDropEntry pick(List<MonsterDropEntry> drops) {
        long total = 0;
        for (MonsterDropEntry drop : drops) {
            if (drop.itemId != 0 && drop.chance > 0) {
                total += drop.chance;
            }
        }
        if (total <= 0) {
            return null;
        }
        long roll = ThreadLocalRandom.current().nextLong(total);
        for (MonsterDropEntry drop : drops) {
            if (drop.itemId != 0 && drop.chance > 0) {
                roll -= drop.chance;
                if (roll < 0) {
                    return drop;
                }
            }
        }
        return null;
    }
}
