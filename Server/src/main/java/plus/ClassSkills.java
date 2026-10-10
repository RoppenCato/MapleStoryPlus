package plus;

import client.Character;
import client.Job;
import client.Skill;
import client.SkillFactory;
import client.keybind.KeyBinding;
import constants.skills.Hermit;

import java.util.HashMap;
import java.util.Map;

/**
 * MapleStoryPlus: class skill rules that the skill data cannot express.
 * <ul>
 * <li>Paired warrior weapon skills (sword and axe, sword and blunt weapon, spear and pole arm) level
 * together, so a warrior pays for a pair once and can switch weapon type.</li>
 * <li>The bandit line gets the Hermit's Flash Jump from 3rd job. The client does not list another job's
 * skill in the skill window, so the server grants it and puts it on a key.</li>
 * </ul>
 */
public class ClassSkills {
    private static final Map<Integer, Integer> TWINS = new HashMap<>();

    private static void pair(int a, int b) {
        TWINS.put(a, b);
        TWINS.put(b, a);
    }

    static {
        // Fighter: mastery, final attack, booster (sword and axe)
        pair(1100000, 1100001); pair(1100002, 1100003); pair(1101004, 1101005);
        // Page (sword and blunt weapon)
        pair(1200000, 1200001); pair(1200002, 1200003); pair(1201004, 1201005);
        // Spearman (spear and pole arm)
        pair(1300000, 1300001); pair(1300002, 1300003); pair(1301004, 1301005);
        // Crusader: Panic, Coma
        pair(1111003, 1111004); pair(1111005, 1111006);
        // White Knight: fire, ice and lightning charges
        pair(1211003, 1211004); pair(1211005, 1211006); pair(1211007, 1211008);
        // Dragon Knight: Crusher, Dragon Fury
        pair(1311001, 1311002); pair(1311003, 1311004);
        // Paladin: Holy Charge, Divine Charge
        pair(1221003, 1221004);
    }

    /** After a point is put into a skill: bring its twin, if it has one, up to the same level. */
    public static void levelTwin(Character chr, Skill skill) {
        Integer twinId = TWINS.get(skill.getId());
        if (twinId == null) {
            return;
        }
        Skill twin = SkillFactory.getSkill(twinId);
        if (twin == null) {
            return;
        }
        byte level = chr.getSkillLevel(skill);
        int master = Math.max(chr.getMasterLevel(skill), chr.getMasterLevel(twin));
        if (chr.getSkillLevel(twin) < level || chr.getMasterLevel(twin) < master) {
            chr.changeSkillLevel(twin, (byte) Math.max(level, chr.getSkillLevel(twin)), master, chr.getSkillExpiration(twin));
        }
    }

    // Keys tried, in order, when Flash Jump is put on the keyboard: V, B, N, G, H.
    private static final int[] FLASH_JUMP_KEYS = {47, 48, 49, 34, 35};
    private static final int KEY_TYPE_SKILL = 1;

    /**
     * Chief Bandits and Shadowers have Flash Jump. Its level follows the character's level, one per level
     * from 70, so it is maxed at level 89; a Hermit spends 20 skill points on the same thing.
     */
    public static void updateBanditFlashJump(Character chr) {
        Job job = chr.getJob();
        if (job != Job.CHIEFBANDIT && job != Job.SHADOWER) {
            return;
        }
        Skill flashJump = SkillFactory.getSkill(Hermit.FLASH_JUMP);
        if (flashJump == null) {
            return;
        }
        int target = Math.max(1, Math.min(flashJump.getMaxLevel(), chr.getLevel() - 69));
        boolean first = chr.getSkillLevel(flashJump) <= 0;
        if (chr.getSkillLevel(flashJump) < target) {
            chr.changeSkillLevel(flashJump, (byte) target, 0, -1);
        }
        if (first) {
            bindFlashJump(chr);
        }
    }

    private static void bindFlashJump(Character chr) {
        Map<Integer, KeyBinding> keymap = chr.getKeymap();
        for (KeyBinding bound : keymap.values()) {
            if (bound.getType() == KEY_TYPE_SKILL && bound.getAction() == Hermit.FLASH_JUMP) {
                return;
            }
        }
        for (int key : FLASH_JUMP_KEYS) {
            if (!keymap.containsKey(key)) {
                chr.changeKeybinding(key, new KeyBinding(KEY_TYPE_SKILL, Hermit.FLASH_JUMP));
                chr.sendKeymap();
                chr.dropMessage(5, "You learned Flash Jump. It is on a free key; open Key Settings to see or move it.");
                return;
            }
        }
        chr.dropMessage(5, "You learned Flash Jump, but no key was free for it. Free one of V, B, N, G or H and change map.");
    }
}
