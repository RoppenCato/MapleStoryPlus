"""Estimates how much equipment a player picks up while levelling, and how much of it is of use to them.

    python Settings/Scripts/Simulate-Drops.py                 every class, per ten levels
    python Settings/Scripts/Simulate-Drops.py --class thief   one class, with the detail per bracket
    python Settings/Scripts/Simulate-Drops.py --levels        one row per level (with --class)
    python Settings/Scripts/Simulate-Drops.py --drop-rate 1   try another drop rate than the one in config.yaml

Nothing is changed and the database is not needed: it reads the reference lists, so run
Settings/Reference/Build-Reference.py first if drops changed.

How it works: at each level the player trains where people train (Hunting-Spots.tsv), or failing that
on crowded monsters a little under their level; the experience table says how many kills the level
takes; the drop table says what those kills give. "For you" is equipment your class can wear that needs
between 9 levels under your level and 3 over it: the things you would actually put on.

    --budget 8     what if: every level gives about 8 pieces of gear, whatever the level. Each monster's
                   chances are scaled so that its kills in one level add up to that. Shows what a rule like
                   that would feel like before it is built.
"""
import argparse
import collections
import io
import math
import os
import re
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(os.path.dirname(HERE))
REF = os.path.join(ROOT, "Settings", "Reference")

LEVELS_BELOW = 7            # without a known hunting spot, a player trains on monsters this far under their level...
LEVELS_ABOVE = 1            # ...to this far above
MIN_SPAWNS = 8
USEFUL_BELOW = 9            # equipment needing up to this many levels under yours still counts as "for you"...
USEFUL_AHEAD = 3            # ...and so does what you can wear within this many levels
CLASSES = ["warrior", "magician", "bowman", "thief", "pirate"]


def rows(name):
    with io.open(os.path.join(REF, name), encoding="utf-8") as f:
        head = f.readline().rstrip("\n").split("\t")
        return [dict(zip(head, line.rstrip("\n").split("\t"))) for line in f]


def config_rate(name):
    with io.open(os.path.join(ROOT, "Settings", "config.yaml"), encoding="utf-8") as f:
        m = re.search(r"^\s*" + name + r":\s*(\d+)", f.read(), re.M)
    return int(m.group(1)) if m else 1


def exp_table():
    path = os.path.join(ROOT, "Server", "src", "main", "java", "constants", "game", "ExpTable.java")
    with io.open(path, encoding="utf-8") as f:
        m = re.search(r"int\[\] exp = \{([^}]*)\}", f.read())
    return [int(x) for x in m.group(1).split(",")]


def main():
    p = argparse.ArgumentParser(description="How much gear drops while levelling")
    p.add_argument("--class", dest="cls", choices=CLASSES)
    p.add_argument("--levels", action="store_true")
    p.add_argument("--drop-rate", type=float)
    p.add_argument("--exp-rate", type=float)
    p.add_argument("--to", type=int, default=120)
    p.add_argument("--budget", type=float, help="what if every level gave about this many pieces of gear")
    p.add_argument("--cap", type=float, default=0.12, help="with --budget: the highest chance of any gear per kill (default 0.12)")
    a = p.parse_args()
    drop_rate = a.drop_rate or config_rate("drop_rate")
    exp_rate = a.exp_rate or config_rate("exp_rate")
    need = exp_table()

    mobs = {r["id"]: r for r in rows("Mobs.tsv") if r["level"].isdigit() and r["exp"].isdigit()}
    spawns = collections.Counter()
    for r in rows("MobSpawns.tsv"):
        if r["count"].isdigit() and r["map_id"].isdigit() and int(r["map_id"]) < 900000000:
            spawns[r["mob_id"]] = max(spawns[r["mob_id"]], int(r["count"]))
    ordinary = [i for i, m in mobs.items() if not m["boss"] and int(i) < 9000000 and int(m["exp"]) > 0 and spawns[i] >= MIN_SPAWNS]
    by_name = collections.defaultdict(list)
    for i in ordinary:
        by_name[mobs[i]["name"].lower()].append(i)
    spots = []
    for r in rows("Hunting-Spots.tsv"):
        found = by_name.get(r["monster"].lower())
        if found:
            spots.append((int(r["player_from"]), int(r["player_to"]), max(found, key=lambda i: spawns[i])))
    equips = {r["id"]: r for r in rows("Equips.tsv") if r["cash"] != "cash" and r["req_level"].isdigit()}
    drops = collections.defaultdict(list)
    for d in rows("Drops.tsv"):
        if d["item_id"] in equips and d["mob_id"] in mobs and d["quest_id"] in ("", "0"):
            drops[d["mob_id"]].append((d["item_id"], min(1.0, float(d["chance_percent"] or 0) / 100 * drop_rate)))

    def fits(item, cls, level):
        e = equips[item]
        return (e["job"] == "all" or cls in e["job"].split("/")) and level - USEFUL_BELOW <= int(e["req_level"]) <= level + USEFUL_AHEAD

    table = []
    for level in range(1, a.to):
        hunted = [mob for start, end, mob in spots if start <= level <= end]
        where = "hunting spot"
        if not hunted:
            hunted = [i for i in ordinary if max(1, level - LEVELS_BELOW) <= int(mobs[i]["level"]) <= level + LEVELS_ABOVE]
            where = "any monster near the level"
        if not hunted:
            continue
        exp = sum(int(mobs[i]["exp"]) for i in hunted) / len(hunted)
        kills = need[level - 1] / (exp * exp_rate)
        row = {"level": level, "kills": kills, "where": where, "any": 0.0,
               "names": ", ".join(sorted({mobs[i]["name"] for i in hunted})[:3])}
        for cls in CLASSES:
            row[cls] = row[cls + "_weapon"] = 0.0
        for mob in hunted:
            share = kills / len(hunted)
            scale = 1.0
            if a.budget:
                per_kill = sum(chance for _, chance in drops[mob])
                wanted = min(a.cap, a.budget / kills)
                scale = wanted / per_kill if per_kill else 0.0
            for item, chance in drops[mob]:
                chance *= scale
                row["any"] += share * chance
                for cls in CLASSES:
                    if fits(item, cls, level):
                        row[cls] += share * chance
                        if equips[item]["type"] == "Weapon" and equips[item]["job"] != "all":
                            row[cls + "_weapon"] += share * chance
        table.append(row)

    size = 1 if a.levels and a.cls else 10
    print(f"Drop rate x{drop_rate:g}, exp rate x{exp_rate:g}. Expected numbers; real play swings around them."
          + (f" WHAT IF: about {a.budget:g} pieces of gear per level, at most 1 kill in {1 / a.cap:.0f}." if a.budget else "") + "\n")
    if a.cls:
        print(f"{a.cls}: equipment picked up while levelling. 'For you' = wearable by a {a.cls}, needing your level or up to {USEFUL_BELOW} under it or {USEFUL_AHEAD} over.\n")
        print(f"{'levels':>8} {'kills':>7} {'any gear':>9} {'kills/drop':>10} | {'for you':>8} {'kills/drop':>10} | {'weapons':>8} {'chance of 1+':>12}   training on")
    else:
        print(f"{'levels':>8} {'kills':>7} {'any gear':>9} {'kills/drop':>10} | pieces for you, and (class weapons): " + "  ".join(f"{c:>14}" for c in CLASSES))
    for start in range(1, a.to, size):
        part = [r for r in table if start <= r["level"] < start + size]
        if not part:
            continue
        total = lambda key: sum(r[key] for r in part)
        label = str(start) if size == 1 else f"{start}-{min(start + size - 1, a.to)}"
        per = lambda n: f"{total('kills') / n:,.0f}" if n > 0.005 else "-"
        line = f"{label:>8} {total('kills'):>7,.0f} {total('any'):>9.1f} {per(total('any')):>10} |"
        if a.cls:
            own, weapons = total(a.cls), total(a.cls + "_weapon")
            names = collections.Counter(n for r in part for n in r["names"].split(", "))
            line += (f" {own:>8.1f} {per(own):>10} | {weapons:>8.2f} {100 * (1 - math.exp(-weapons)):>11.0f}%   "
                     + ", ".join(n for n, _ in names.most_common(3)))
        else:
            line += " " * 38 + "  ".join(f"{total(c):>6.1f} ({total(c + '_weapon'):>4.1f})" for c in CLASSES)
        print(line)


if __name__ == "__main__":
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")
    main()
