"""Sizes the trial bosses for one player: sets each boss's HP so that the fight takes a set time.

    python Settings/Scripts/Tune-Bosses.py --check     show the table, write nothing
    python Settings/Scripts/Tune-Bosses.py             write the HP into the server's monster data

The bosses are the ones in Settings/Trials.tsv. For each, the damage simulator (Simulate-Damage.py) says
what a middling class does per second on one monster at the level the fight is meant for; the boss gets
that much times the length of the fight. Restart the server afterwards; run it again after changing
skills, because the bosses follow the damage.

HP is the server's alone to decide, so no client change is needed. How hard a boss hits is in the client
and is not touched. Experience and drops are left as they are.

What is assumed is in the block below.
"""
import argparse
import importlib.util
import io
import os
import re
import subprocess
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(os.path.dirname(HERE))
MOB_WZ = os.path.join(ROOT, "Server", "wz", "Mob.wz")

# ---------------------------------------------------------------------------------------------
# Assumptions
# ---------------------------------------------------------------------------------------------
SECONDS = 100           # an ordinary trial boss: a fight of about a minute and a half
SECONDS_HARDEST = 300   # the three highest of a band: about five minutes
SECONDS_BAND_1 = 75     # the two bosses before 2nd job are a first taste
REAL_SHARE = 0.75       # share of the simulator's damage a player really lands: misses, moving, the boss's defence
# The level a fight is meant for: the boss's own level, but never above what the band's job needs
BAND_TOP = {1: 28, 2: 68, 3: 118, 4: 160}
ORIGINAL_COMMIT = "47b61b538"   # the server as it was copied, to show what the HP used to be


def load(name):
    spec = importlib.util.spec_from_file_location(name.replace("-", "_"), os.path.join(HERE, name + ".py"))
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def mob_file(mob_id):
    return os.path.join(MOB_WZ, f"{mob_id:07d}.img.xml")


def original_hp(mob_id):
    out = subprocess.run(["git", "-C", os.path.join(ROOT, "Server"), "show", f"{ORIGINAL_COMMIT}:wz/Mob.wz/{mob_id:07d}.img.xml"],
                         capture_output=True, text=True, encoding="utf-8", errors="ignore")
    m = re.search(r'<int name="maxHP" value="(\d+)"/>', out.stdout or "")
    return int(m.group(1)) if m else 0


def main():
    p = argparse.ArgumentParser(description="Size the trial bosses for one player")
    p.add_argument("--check", action="store_true")
    a = p.parse_args()
    sim = load("Simulate-Damage")
    data, skills = sim.mc.Data(), sim.load_skills()

    bosses = []
    with io.open(os.path.join(ROOT, "Settings", "Trials.tsv"), encoding="utf-8") as f:
        f.readline()
        for line in f:
            cell = line.rstrip("\n").split("\t")
            if len(cell) >= 3 and cell[0] in ("1", "2", "3"):
                with io.open(mob_file(int(cell[1])), encoding="utf-8") as m:
                    text = m.read()
                level = int(re.search(r'<int name="level" value="(\d+)"/>', text).group(1))
                bosses.append({"band": int(cell[0]), "id": int(cell[1]), "name": cell[2], "level": level,
                               "hp": int(re.search(r'<int name="maxHP" value="(\d+)"/>', text).group(1))})
    for band in (1, 2, 3):
        top = sorted((b for b in bosses if b["band"] == band), key=lambda b: (b["level"], b["id"]))[-3:]
        for b in bosses:
            if b["band"] == band:
                b["seconds"] = SECONDS_BAND_1 if band == 1 else SECONDS_HARDEST if b in top else SECONDS
                b["fight_level"] = max(10, min(b["level"], BAND_TOP[band]))

    print(f"{'boss':<18} {'level':>5} {'fight at':>8} {'damage/s':>9} {'fight':>6} {'HP was':>12} {'HP now':>12}")
    changed = 0
    for b in bosses:
        damage = sim.typical_damage(data, skills, b["fight_level"]) * REAL_SHARE
        hp = int(round(damage * b["seconds"], -2 if damage * b["seconds"] < 100000 else -3))
        was = original_hp(b["id"]) or b["hp"]
        print(f"{b['name']:<18} {b['level']:>5} {b['fight_level']:>8} {damage:>9,.0f} {b['seconds']:>5}s {was:>12,} {hp:>12,}")
        if hp != b["hp"] and not a.check:
            path = mob_file(b["id"])
            with io.open(path, encoding="utf-8", newline="") as f:
                text = f.read()
            text = re.sub(r'(<int name="maxHP" value=")\d+("/>)', lambda m: m.group(1) + str(hp) + m.group(2), text, count=1)
            with io.open(path, "w", encoding="utf-8", newline="") as f:
                f.write(text)
            changed += 1
    print("\nCheck only: nothing written." if a.check else f"\n{changed} bosses changed. Restart the server to load them.")


if __name__ == "__main__":
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")
    main()
