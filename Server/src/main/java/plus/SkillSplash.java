package plus;

import client.Character;
import client.Skill;
import client.status.MonsterStatus;
import client.status.MonsterStatusEffect;
import constants.skills.Archer;
import constants.skills.Assassin;
import constants.skills.Cleric;
import constants.skills.FPWizard;
import constants.skills.Magician;
import server.StatEffect;
import server.TimerManager;
import server.life.Monster;
import server.maps.MapleMap;
import tools.PacketCreator;

import java.awt.Point;
import java.util.ArrayList;
import java.util.Comparator;
import java.util.List;
import java.util.Map;
import java.util.Set;

/**
 * MapleStoryPlus: extra targets for skills the client keeps on one monster.
 * <p>
 * The client decides which monsters a spell or ranged attack hits, and for these skills it always picks one,
 * whatever target count the skill data gives. So the server adds the rest: when one of these skills damages
 * a monster, the nearest monsters around it take the same damage, up to the skill's target count
 * ({@code mobCount} in the server's skill data).
 */
public class SkillSplash {
    private static final Set<Integer> SKILLS = Set.of(
            Magician.ENERGY_BOLT, FPWizard.POISON_BREATH, Cleric.HOLY_ARROW, Archer.ARROW_BLOW, Assassin.DRAIN);

    // How far from the monster that was hit another monster may stand, in pixels.
    private static final int REACH_X = 200;
    private static final int REACH_Y = 80;
    // The extra damage lands a little after the hit, about when the projectile arrives.
    private static final long DELAY_MS = 350;

    /** Called after a single-target hit has been applied to {@code hit}. */
    public static void apply(Character player, MapleMap map, Monster hit, Skill skill, StatEffect effect, int damage) {
        if (skill == null || effect == null || damage <= 0 || !SKILLS.contains(skill.getId())) {
            return;
        }
        int extra = effect.getMobCount() - 1;
        if (extra <= 0) {
            return;
        }

        Point at = hit.getPosition();
        List<Monster> near = new ArrayList<>();
        for (Monster m : map.getAllMonsters()) {
            if (m == hit || !m.isAlive() || m.isFake()) {
                continue;
            }
            Point p = m.getPosition();
            if (Math.abs(p.x - at.x) <= REACH_X && Math.abs(p.y - at.y) <= REACH_Y) {
                near.add(m);
            }
        }
        near.sort(Comparator.comparingDouble(m -> m.getPosition().distanceSq(at)));

        Map<MonsterStatus, Integer> stati = effect.getMonsterStati();
        for (Monster m : near.subList(0, Math.min(extra, near.size()))) {
            // The same damage as the first monster took, give or take 10%.
            int dealt = Math.max(1, (int) (damage * (0.9 + Math.random() * 0.2)));
            TimerManager.getInstance().schedule(() -> {
                if (!m.isAlive() || player.getMap() != map) {
                    return;
                }
                map.broadcastMessage(PacketCreator.damageMonster(m.getObjectId(), dealt), m.getPosition());
                if (!stati.isEmpty() && effect.makeChanceResult()) {
                    m.applyStatus(player, new MonsterStatusEffect(stati, skill, null, false), effect.isPoison(), effect.getDuration());
                }
                map.damageMonster(player, m, dealt);
            }, DELAY_MS);
        }
    }
}
