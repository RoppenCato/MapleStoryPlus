"""Decides which equipment ordinary monsters drop and how often, by rule.

    python Settings/Scripts/Rebalance-Drops.py --check     show what would change, write nothing
    python Settings/Scripts/Rebalance-Drops.py             apply (saves a database backup first)

The database must be running and the game server stopped. Running it twice changes nothing the second
time. Afterwards run  python Settings/Reference/Build-Reference.py  and  Make-Drop-Site.py, and look at
the result with  Simulate-Drops.py.

The rules. Only weapons and armour dropped by ordinary monsters are touched; bosses, event and party
quest monsters, scrolls, ores, potions and quest items are left alone.

WHICH MONSTERS DROP AN ITEM that needs level L
  1. None more than TOO_HIGH levels above L or TOO_LOW below. A level 70 dagger is found while you are
     about 60 to 72. The top tier (level TOP_TIER and up) is the exception: nothing better exists for
     ordinary monsters to drop, so it also drops from everything above it.
  2. At least WANTED monsters between L - BAND_BELOW and L + BAND_ABOVE, chosen from the popular hunting
     spots first (Settings/Reference/Hunting-Spots.tsv), then from the monsters with the fewest drops.
     This covers every item ordinary monsters already drop, and the plain gear of every class
     (Settings/Reference/Loadouts.tsv) even where nothing dropped it before.
  3. Every monster that lives in numbers has something for every class: at least one weapon and
     ARMOUR_PER_CLASS pieces of armour that a warrior, a magician, a bowman, a thief and a pirate can use
     around its level.

HOW OFTEN
  4. A budget, not a flat chance. A level takes 50 kills at level 10 and 3,000 at level 70; with the same
     chance per kill, gear floods in at high level. So each monster's total chance of dropping gear is set
     so that one level's worth of kills gives about PIECES_PER_LEVEL pieces at a popular hunting spot and
     PIECES_ELSEWHERE anywhere else, and never more often than 1 kill in 1/MOST_PER_KILL.
  5. Within a monster the five classes and the gear everyone can wear get equal shares, gear of the
     right level counts double against gear the monster's hunters have outgrown, and the very first gear
     (level STARTER_ITEM_LEVEL or less, on monsters up to level STARTER_MOB_LEVEL) counts five times.

The chances are worked out for the drop and exp rates in Settings/config.yaml. After changing those
rates, run this again.
"""
import argparse
import collections
import datetime
import io
import os
import re
import subprocess
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(os.path.dirname(HERE))
REF = os.path.join(ROOT, "Settings", "Reference")
MYSQL = os.path.join(ROOT, "Tools", "mysql", "bin")
MYINI = "--defaults-file=" + os.path.join(ROOT, "Settings", "mysql.ini")

BAND_BELOW = 10         # a monster up to this many levels under the item's level is "around that level"
BAND_ABOVE = 2
TOO_HIGH = 5            # drops from monsters further above the item's level than this are removed
TOO_LOW = 20            # ...and further below than this
TOP_TIER = 95           # items needing this level or more also drop from every ordinary monster above them
WANTED = 3              # monsters around its level that should drop each item
MAX_PER_MONSTER = 28    # rule 2 gives no monster more equipment drops than this
MIN_SPAWNS = 8          # a monster must live in at least this number on one ordinary map to be given drops
ARMOUR_PER_CLASS = 2    # rule 3: pieces of armour per class on every such monster, next to one weapon
PIECES_PER_LEVEL = 8.0  # rule 4: gear per level of training at a popular hunting spot
PIECES_ELSEWHERE = 5.5  # ...and anywhere else
MOST_PER_KILL = 0.12    # no monster drops gear more often than this (1 kill in 8)
STARTER_ITEM_LEVEL = 12
STARTER_MOB_LEVEL = 10
CLASSES = ("warrior", "magician", "bowman", "thief", "pirate")
ARMOUR = ("Cap", "Coat", "Longcoat", "Pants", "Shoes", "Glove", "Shield")


def rows(name):
    with io.open(os.path.join(REF, name), encoding="utf-8") as f:
        head = f.readline().rstrip("\n").split("\t")
        return [dict(zip(head, line.rstrip("\n").split("\t"))) for line in f]


def sql(statement):
    out = subprocess.run([os.path.join(MYSQL, "mysql"), MYINI, "cosmic", "-N", "-e", statement], capture_output=True, text=True)
    if out.returncode:
        raise SystemExit("Database error (is it running?):\n" + out.stderr[:500])
    return [line.split("\t") for line in out.stdout.splitlines()]


def config_rate(name):
    with io.open(os.path.join(ROOT, "Settings", "config.yaml"), encoding="utf-8") as f:
        m = re.search(r"^\s*" + name + r":\s*(\d+)", f.read(), re.M)
    return int(m.group(1)) if m else 1


def exp_table():
    path = os.path.join(ROOT, "Server", "src", "main", "java", "constants", "game", "ExpTable.java")
    with io.open(path, encoding="utf-8") as f:
        m = re.search(r"int\[\] exp = \{([^}]*)\}", f.read())
    return [int(x) for x in m.group(1).split(",")]


def plan():
    equips = {int(r["id"]): r for r in rows("Equips.tsv") if r["cash"] != "cash" and r["req_level"].isdigit()}
    mobs = {int(r["id"]): r for r in rows("Mobs.tsv") if r["level"].isdigit()}
    spawns = collections.Counter()
    for r in rows("MobSpawns.tsv"):
        if r["count"].isdigit() and r["map_id"].isdigit() and int(r["map_id"]) < 900000000:
            spawns[int(r["mob_id"])] = max(spawns[int(r["mob_id"])], int(r["count"]))
    ordinary = {i for i, m in mobs.items() if not m["boss"] and i < 9000000 and int(m["exp"] or 0) > 0}
    crowded = sorted(i for i in ordinary if spawns[i] >= MIN_SPAWNS)
    names = collections.defaultdict(list)
    for i in crowded:
        names[mobs[i]["name"].lower()].append(i)
    popular = {}                                            # monster -> the level people train on it
    for r in rows("Hunting-Spots.tsv"):
        found = names.get(r["monster"].lower())
        if found:
            popular[max(found, key=lambda i: spawns[i])] = (int(r["player_from"]) + int(r["player_to"])) // 2
    level = lambda mob: int(mobs[mob]["level"])
    need = lambda item: int(equips[item]["req_level"])
    loadouts = {int(r["item_id"]) for r in rows("Loadouts.tsv") if r["item_id"].isdigit() and int(r["item_id"]) in equips}

    def around(mob, item):                                  # is the monster "around the level" of the item
        top = need(item) >= TOP_TIER and level(mob) > need(item)
        return need(item) - BAND_BELOW <= level(mob) <= need(item) + BAND_ABOVE or top

    def allowed(mob, item):
        gap = level(mob) - need(item)
        return -TOO_LOW <= gap <= TOO_HIGH or (need(item) >= TOP_TIER and gap > 0)

    # What is there now
    have = collections.defaultdict(dict)                    # monster -> item -> (row id, chance)
    delete = []
    for row_id, mob, item, chance in sql("SELECT id, dropperid, itemid, chance FROM drop_data WHERE questid = 0 "
                                         "AND itemid >= 1000000 AND itemid < 2000000 ORDER BY id"):
        row_id, mob, item, chance = int(row_id), int(mob), int(item), int(chance)
        if item not in equips or mob not in ordinary:
            continue
        if item in have[mob]:
            delete.append(row_id)                           # the same item twice on one monster
        else:
            have[mob][item] = (row_id, chance)
    known = set(loadouts)
    for mob in have:
        known.update(have[mob])

    # Rule 1
    removed = 0
    for mob in list(have):
        for item in list(have[mob]):
            if 10 <= need(item) <= 120 and not allowed(mob, item):
                delete.append(have[mob].pop(item)[0])
                removed += 1

    added = collections.defaultdict(set)                    # monster -> items it is given
    count = lambda mob: len(have[mob]) + len(added[mob])
    droppers = collections.defaultdict(set)
    for mob in have:
        for item in have[mob]:
            droppers[item].add(mob)

    def give(mob, item):
        added[mob].add(item)
        droppers[item].add(mob)

    # Rule 2
    for item in sorted(known):
        if not 10 <= need(item) <= 120:
            continue
        near = [m for m in droppers[item] if around(m, item)]
        choice = [m for m in crowded if around(m, item) and m not in droppers[item] and count(m) < MAX_PER_MONSTER]
        choice.sort(key=lambda m: (m not in popular, count(m), (m * 31 + item) % 97, m))
        for mob in choice[:max(0, WANTED - len(near))]:
            give(mob, item)

    # Rule 3
    by_class = collections.defaultdict(list)
    for item in sorted(known):
        e = equips[item]
        if e["job"] != "all" and (e["type"] == "Weapon" or e["type"] in ARMOUR):
            for cls in e["job"].split("/"):
                by_class[(cls, e["type"] == "Weapon")].append(item)
    for mob in crowded:
        mine = set(have[mob]) | added[mob]
        for cls in CLASSES:
            for weapon, wanted in ((True, 1), (False, ARMOUR_PER_CLASS)):
                fits = lambda item: around(mob, item) and allowed(mob, item)
                got = sum(1 for item in mine if item in by_class[(cls, weapon)] and fits(item))
                choice = [item for item in by_class[(cls, weapon)] if item not in mine and fits(item)]
                # The plain gear of the class first, then what the fewest monsters drop, then nearest in level
                choice.sort(key=lambda item: (item not in loadouts, len(droppers[item]), abs(need(item) - level(mob) - 3), item))
                for item in choice[:max(0, wanted - got)]:
                    give(mob, item)
                    mine.add(item)

    # Rules 4 and 5
    exp_need, drop_rate, exp_rate = exp_table(), config_rate("drop_rate"), config_rate("exp_rate")
    update, insert = [], []
    for mob in sorted(set(have) | set(added)):
        items = sorted(set(have[mob]) | added[mob])
        if not items:
            continue
        hunter = max(1, min(120, popular.get(mob, level(mob) + 3)))
        kills = exp_need[hunter - 1] / (int(mobs[mob]["exp"]) * exp_rate)
        pieces = PIECES_PER_LEVEL if mob in popular else PIECES_ELSEWHERE
        per_kill = min(MOST_PER_KILL, pieces / kills) / drop_rate          # before the drop rate is applied
        bucket = lambda item: equips[item]["job"].split("/")[0]
        sizes = collections.Counter(bucket(item) for item in items)
        weight = {}
        for item in items:
            w = 1.0 / sizes[bucket(item)]
            w *= 2 if around(mob, item) else 1
            w *= 5 if need(item) <= STARTER_ITEM_LEVEL and level(mob) <= STARTER_MOB_LEVEL else 1
            weight[item] = w
        total = sum(weight.values())
        for item in items:
            chance = max(1, round(1000000 * per_kill * weight[item] / total))
            if item in have[mob]:
                if have[mob][item][1] != chance:
                    update.append((have[mob][item][0], chance))
            else:
                insert.append((mob, item, chance))
    return delete, removed, insert, update, equips, mobs, popular


def main():
    p = argparse.ArgumentParser(description="Which equipment ordinary monsters drop, and how often")
    p.add_argument("--check", action="store_true")
    a = p.parse_args()
    delete, removed, insert, update, equips, mobs, popular = plan()
    print(f"Popular hunting monsters found: {len(popular)}")
    print(f"Drops removed: {len(delete)} ({removed} too far from the item's level, {len(delete) - removed} doubles)")
    print(f"Drops added: {len(insert)}")
    print(f"Chances changed: {len(update)}")
    for mob, item, chance in insert[:5]:
        print(f"   e.g. {equips[item]['name']} (level {equips[item]['req_level']}) now also from {mobs[mob]['name']} (level {mobs[mob]['level']})")
    if a.check or not (delete or insert or update):
        print("Check only: nothing changed." if a.check else "Nothing to do.")
        return
    if sql("SELECT COUNT(*) FROM accounts WHERE loggedin <> 0")[0][0] != "0":
        raise SystemExit("Someone is logged in. Stop the game server first.")
    stamp = datetime.datetime.now().strftime("%Y-%m-%d_%H%M%S")
    backup = os.path.join(ROOT, "Backups", f"cosmic_{stamp}_before-drops.sql")
    os.makedirs(os.path.dirname(backup), exist_ok=True)
    out = subprocess.run([os.path.join(MYSQL, "mysqldump"), MYINI, "--single-transaction", "--routines", "--databases",
                          "cosmic", "--result-file=" + backup], capture_output=True, text=True)
    if out.returncode:
        raise SystemExit("Backup failed, nothing changed:\n" + out.stderr)
    print("Backup: " + backup)
    statements = []
    for i in range(0, len(delete), 500):
        statements.append("DELETE FROM drop_data WHERE id IN (" + ",".join(map(str, delete[i:i + 500])) + ")")
    by_chance = collections.defaultdict(list)
    for row_id, chance in update:
        by_chance[chance].append(row_id)
    for chance, ids in by_chance.items():
        for i in range(0, len(ids), 500):
            statements.append(f"UPDATE drop_data SET chance = {chance} WHERE id IN (" + ",".join(map(str, ids[i:i + 500])) + ")")
    for i in range(0, len(insert), 300):
        values = ",".join(f"({mob},{item},1,1,0,{chance})" for mob, item, chance in insert[i:i + 300])
        statements.append("INSERT INTO drop_data (dropperid, itemid, minimum_quantity, maximum_quantity, questid, chance) VALUES " + values)
    path = os.path.join(os.environ.get("TEMP", "."), "mapleplus-drops.sql")
    with io.open(path, "w", encoding="utf-8") as f:
        f.write("START TRANSACTION;\n" + ";\n".join(statements) + ";\nCOMMIT;\n")
    with io.open(path, encoding="utf-8") as f:
        out = subprocess.run([os.path.join(MYSQL, "mysql"), MYINI, "cosmic"], stdin=f, capture_output=True, text=True)
    if out.returncode:
        raise SystemExit("Could not apply:\n" + out.stderr[:500])
    print("Applied.")


if __name__ == "__main__":
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")
    main()
