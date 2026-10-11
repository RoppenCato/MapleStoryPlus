"""Estimates the damage of each class at set levels, to compare classes and check the damage rules.

    python Settings/Scripts/Simulate-Damage.py                     every class at levels 30, 50, 70 and 100
    python Settings/Scripts/Simulate-Damage.py --levels 70 119      other levels (10 to 119)
    python Settings/Scripts/Simulate-Damage.py --rules              per class: does a new job's attack beat the old one?

Nothing is changed and the database is not needed.

What is real data: the skill numbers (from the server's skill data, through SkillDetails.tsv), the gear a
character of that class and level wears (the same loadouts Make-Character.py gives out), the weapon's
attack, and the game's damage formulas for version 83.

What is assumed is in the block below: how many attacks a second each weapon manages, and which skill a
class uses. The per-second column stands or falls with those; the per-use column does not.

Not counted: monster defence and level difference, elemental weakness, attack potions, and scrolled gear.
So the numbers are for comparing classes with each other, not for predicting a number on the screen.
"""
import argparse
import importlib.util
import io
import os
import re
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(os.path.dirname(HERE))
REF = os.path.join(ROOT, "Settings", "Reference")

spec = importlib.util.spec_from_file_location("make_character", os.path.join(HERE, "Make-Character.py"))
mc = importlib.util.module_from_spec(spec)
spec.loader.exec_module(mc)

# ---------------------------------------------------------------------------------------------
# Assumptions
# ---------------------------------------------------------------------------------------------
# The game's weapon multiplier, the second stat, and attacks a second with the class's booster on.
WEAPON = {
    "hero":       (4.6, "dex", 1.45), "paladin":   (4.0, "dex", 1.60), "darkknight": (5.0, "dex", 1.45),
    "hunter":     (3.4, "str", 1.45), "crossbow":  (3.6, "str", 1.35), "assassin":   (3.6, "dex", 1.65),
    "bandit":     (3.6, "dex", 1.40), "brawler":   (4.8, "dex", 1.60), "gunslinger": (3.6, "str", 1.45),
    "fp":         (None, None, 1.25), "il":        (None, None, 1.25), "cleric":     (None, None, 1.25),
}
STAR_ATTACK = [(10, 15), (30, 19), (50, 21), (70, 23)]     # (from level, attack of the throwing stars used)
ARROW_ATTACK = [(10, 0), (30, 1), (70, 4)]
MASTERY_FIRST_JOB = 10          # percent, before a weapon mastery skill
MASTERY_WITH_SKILL = 60         # percent, with the 2nd job mastery skill maxed
CRIT_FLAT = (40, 150)           # every class without its own crit: chance %, damage %
CRIT_OWN = {"hunter": (50, 200), "crossbow": (50, 200), "assassin": (50, 200)}   # Critical Shot, Critical Throw (from level 30 for assassins)

# Which attack a class uses on one monster and on a group, per job: (single, group). Skill ids.
ATTACKS = {
    "hero":       {1: (1001004, 1001005), 2: (1001004, 1001005), 3: (1111003, 1111005)},
    "paladin":    {1: (1001004, 1001005), 2: (1001004, 1001005), 3: (1211002, 1211002)},
    "darkknight": {1: (1001004, 1001005), 2: (1001004, 1001005), 3: (1311001, 1311003)},
    "fp":         {1: (2001005, 2001004), 2: (2101004, 2101005), 3: (2111006, 2111002)},
    "il":         {1: (2001005, 2001004), 2: (2201004, 2201005), 3: (2211003, 2211002)},
    "cleric":     {1: (2001005, 2001004), 2: (2301005, 2301005), 3: (2301005, 2311004)},
    "hunter":     {1: (3001005, 3001004), 2: (3001005, 3001004), 3: (3111006, 3111004)},
    "crossbow":   {1: (3001005, 3001004), 2: (3001005, 3201005), 3: (3211006, 3211004)},
    "assassin":   {1: (4001344, 4001344), 2: (4001344, 4101005), 3: (4001344, 4111005)},
    "bandit":     {1: (4001334, 4001334), 2: (4201005, 4201004), 3: (4211002, 4211004)},
    "brawler":    {1: (5001001, 5001002), 2: (5101003, 5101004), 3: (5101003, 5111006)},
    "gunslinger": {1: (5001003, 5001003), 2: (5001003, 5201001), 3: (5210000, 5211004)},
}
# Things that multiply every attack once the class has them: (line, from level, factor, what)
MULTIPLIERS = [("hero", 70, 1.2, "Combo Attack"), ("paladin", 70, 1.3, "element charge"),
               ("assassin", 70, 1.7, "Shadow Partner"), ("fp", 70, 1.4, "Element Amplification"),
               ("il", 70, 1.4, "Element Amplification")]
MEDITATION = 20                 # magic attack from the Fire/Poison and Ice/Lightning wizard's buff, from level 30


def step(steps, level):
    value = steps[0][1]
    for start, v in steps:
        if level >= start:
            value = v
    return value


def load_skills():
    skills = {}
    with io.open(os.path.join(REF, "SkillDetails.tsv"), encoding="utf-8") as f:
        head = f.readline().rstrip("\n").split("\t")
        for line in f:
            r = dict(zip(head, line.rstrip("\n").split("\t")))
            skills.setdefault(int(r["skill_id"]), {})[int(r["level"])] = r
    return skills


def per_use(row):
    """(percent or magic attack per hit, hits, monsters, magic?) of a skill at one level."""
    bullets = re.search(r"bulletCount=(\d+)", row["other"])
    hits = int(row["attackCount"] or (bullets.group(1) if bullets else 1))
    magic = not row["damage"] and bool(row["mad"])
    return int(row["mad"] if magic else row["damage"]), hits, int(row["mobCount"] or 1), magic


def character(data, line, level):
    gear = mc.loadout(data, line, level, 0)
    stats, _ = mc.stats_for(line, level, gear)
    attack = magic = 0
    for item, _ in gear.values():
        for name, value in re.findall(r"(\w+)\+(\d+)", item.get("stats", "")):
            if name == "PAD":
                attack += int(value)
            elif name == "MAD":
                magic += int(value)
            elif name in ("STR", "DEX", "INT", "LUK"):
                stats[name.lower()] += int(value)
    if line == "assassin":
        attack += step(STAR_ATTACK, level)
    if line in ("hunter", "crossbow"):
        attack += step(ARROW_ATTACK, level)
    if line in ("fp", "il") and level >= 30:
        magic += MEDITATION
    return stats, attack, magic


def average_hit(line, level, stats, attack, magic_attack, skill_row):
    """Average damage of one hit line of a skill, before crit."""
    value, hits, mobs, magic = per_use(skill_row)
    if magic:
        matk = stats["int"] + magic_attack
        mastery = int(skill_row["mastery"] or 10) / 100
        high = ((matk * matk / 1000 + matk) / 30 + stats["int"] / 200) * value
        low = ((matk * matk / 1000 + matk * mastery * 0.9) / 30 + stats["int"] / 200) * value
        return (high + low) / 2, value
    multiplier, second, _ = WEAPON[line]
    main = stats[mc.LINES[line][4]]
    other = stats[second] if line not in ("assassin", "bandit") else stats["dex"] + stats["str"]
    mastery = (MASTERY_WITH_SKILL if level >= 30 else MASTERY_FIRST_JOB) / 100
    high = (multiplier * main + other) * attack / 100
    low = (multiplier * main * 0.9 * mastery + other) * attack / 100
    return (high + low) / 2 * value / 100, value


def crit_for(line, level):
    if line in CRIT_OWN and (line != "assassin" or level >= 30):
        return CRIT_OWN[line]
    return CRIT_FLAT if level >= 10 else (0, 100)


def use_damage(line, level, stats, attack, magic_attack, row):
    """Average damage of one use of a skill on one monster, with crit and the class's multiplier."""
    hit, value = average_hit(line, level, stats, attack, magic_attack, row)
    _, hits, mobs, magic = per_use(row)
    chance, strength = crit_for(line, level)
    if not magic and value:
        hit *= 1 + chance / 100 * (strength - 100) / value          # a crit adds a flat amount to each hit line
    for who, start, factor, _ in MULTIPLIERS:
        if who == line and level >= start:
            hit *= factor
    return hit * hits, mobs


def tier(level):
    return 1 if level < 30 else 2 if level < 70 else 3


def main():
    p = argparse.ArgumentParser(description="Estimate class damage")
    p.add_argument("--levels", type=int, nargs="+", default=[30, 50, 70, 100])
    p.add_argument("--rules", action="store_true", help="check the two damage rules per class")
    a = p.parse_args()
    data, skills = mc.Data(), load_skills()

    if a.rules:
        print("Does a new job's attack at level 1 beat the old job's attack at max? Total percent (or magic attack) per use.\n")
        print(f"{'class':<11} {'old attack':<24} {'max':>6}   {'new attack':<24} {'level 1':>8} {'max':>6}  rule")
        for line, by_tier in ATTACKS.items():
            for kind, name in ((0, "single"), (1, "group")):
                chain = []
                for t in (1, 2, 3):
                    sid = by_tier[t][kind]
                    if not chain or chain[-1] != sid:
                        chain.append(sid)
                for old, new in zip(chain, chain[1:]):
                    o, n = skills[old], skills[new]
                    total = lambda row: per_use(row)[0] * per_use(row)[1]
                    old_max, new_first, new_max = total(o[max(o)]), total(n[1]), total(n[max(n)])
                    verdict = "ok" if new_first > old_max else ("group, fewer or more targets" if kind else "BELOW")
                    print(f"{line:<11} {o[1]['skill'][:24]:<24} {old_max:>6}   {n[1]['skill'][:24]:<24} {new_first:>8} {new_max:>6}  {verdict} ({name})")
        return

    print("Average damage per use on one monster, and per second, with every skill of the job maxed.")
    print("Gear is the plain shop and drop gear for the level, unscrolled. Assumptions are at the top of the script.\n")
    print(f"{'level':>5} {'class':<11} {'single-target attack':<22} {'per use':>9} {'per sec':>9}   {'group attack':<22} {'per mob':>9} {'mobs':>4} {'per sec, all':>12}")
    for level in a.levels:
        results = []
        for line in mc.LINES:
            stats, attack, magic_attack = character(data, line, level)
            single_id, group_id = ATTACKS[line][tier(level)]
            rate = WEAPON[line][2]
            single_row = skills[single_id][max(skills[single_id])]
            group_row = skills[group_id][max(skills[group_id])]
            single, _ = use_damage(line, level, stats, attack, magic_attack, single_row)
            group, mobs = use_damage(line, level, stats, attack, magic_attack, group_row)
            results.append((single * rate, line, single_row["skill"], single, group_row["skill"], group, mobs, rate))
        best = max(r[0] for r in results)
        for per_second, line, s_name, single, g_name, group, mobs, rate in sorted(results, reverse=True):
            bar = "#" * round(12 * per_second / best)
            print(f"{level:>5} {line:<11} {s_name[:22]:<22} {single:>9,.0f} {per_second:>9,.0f}   {g_name[:22]:<22} {group:>9,.0f} {mobs:>4} {group * mobs * rate:>12,.0f}  {bar}")
        print()


if __name__ == "__main__":
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")
    main()
