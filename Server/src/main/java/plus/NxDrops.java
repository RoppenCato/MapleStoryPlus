package plus;

import client.Character;
import constants.game.ExpTable;
import constants.id.ItemId;
import server.life.Monster;

/**
 * MapleStoryPlus: NX is earned by playing, and at an even pace.
 * <p>
 * Any monster can drop an NX card (100 NX, and a tenth as often 250 NX). A flat chance per kill would
 * give almost nothing in the first levels, which take a few dozen kills each, and a flood later, where
 * a level takes thousands. So the chance follows the monster: one level's worth of kills gives about
 * {@link #NX_PER_LEVEL} NX whatever the level, which is enough for a pet and its gear in the teens and
 * a steady income after. Bosses are worth ten ordinary monsters of their level.
 */
public class NxDrops {
    /** NX a level of training gives, from level 10 on. Before that the cap below keeps it lower. */
    public static final int NX_PER_LEVEL = 1500;
    /** No ordinary monster drops a 100 NX card more often than this (15%). */
    private static final double MOST_PER_KILL = 0.15;
    private static final int BOSS_TIMES = 10;
    /** One 100 NX card and a tenth of a 250 NX card: what a "card chance" of 1 is worth in NX. */
    private static final double NX_PER_CARD_CHANCE = 100 + 250 / 10.0;

    /** The chance, out of 1,000,000, that this monster drops the given NX card for this player. */
    public static int chance(int cardId, Monster mob, Character chr) {
        if (mob.getExp() <= 0) {
            return 0;
        }
        // The level of the players who train on this monster, and the kills that level takes them
        int hunter = Math.max(1, Math.min(199, mob.getLevel() + 3));
        double kills = ExpTable.getExpNeededForLevel(hunter) / ((double) mob.getExp() * Math.max(1, chr.getRawExpRate()));
        double card = Math.min(MOST_PER_KILL, NX_PER_LEVEL / (Math.max(1.0, kills) * NX_PER_CARD_CHANCE));
        if (mob.isBoss()) {
            card = Math.min(1.0, card * BOSS_TIMES);
        }
        if (cardId == ItemId.NX_CARD_250) {
            card /= 10;
        }
        return (int) Math.round(card * 1000000);
    }
}
