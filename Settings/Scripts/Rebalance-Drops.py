"""Makes equipment drop from monsters around its own level, and favours the popular hunting spots.

    python Settings/Scripts/Rebalance-Drops.py --check     show what would change, write nothing
    python Settings/Scripts/Rebalance-Drops.py             apply (saves a database backup first)

The database must be running and the game server stopped. Running it twice changes nothing the second
time. Afterwards run  python Settings/Reference/Build-Reference.py  and  Make-Drop-Site.py.

The rules, for a weapon or armour that needs level L (only items that ordinary monsters already drop;
cash items, boss-only items and items nothing drops are left alone):

  1. It does not drop from ordinary monsters more than TOO_HIGH levels above L, or more than TOO_LOW below.
     So a level 70 dagger is found while you are about 60 to 72, never at 90.
  2. At least WANTED ordinary monsters between L - BAND_BELOW and L + BAND_ABOVE drop it. Missing ones are
     added: monsters of a popular hunting spot (Settings/Reference/Hunting-Spots.tsv) first, then the
     ones with the fewest equipment drops so far.
  3. At a popular hunting spot, equipment of the right level drops at least at POPULAR_CHANCE.

Bosses and everything that is not equipment (scrolls, ores, potions, quest items) are not touched.
"""
import argparse
import collections
import datetime
import io
import os
import subprocess
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(os.path.dirname(HERE))
REF = os.path.join(ROOT, "Settings", "Reference")
MYSQL = os.path.join(ROOT, "Tools", "mysql", "bin")
MYINI = "--defaults-file=" + os.path.join(ROOT, "Settings", "mysql.ini")

BAND_BELOW = 10         # a monster up to this many levels under the item's level is "around that level"
BAND_ABOVE = 2
TOO_HIGH = 5            # drops from ordinary monsters further above the item's level than this are removed
TOO_LOW = 20            # ...and further below than this
WANTED = 3              # ordinary monsters in the band that should drop each item
MAX_PER_MONSTER = 28    # no monster is given more equipment drops than this by rule 2
MIN_SPAWNS = 8          # a monster must live in at least this number on one ordinary map to be given drops
NEW_CHANCE = 800        # out of 1,000,000 before the drop rate: 0.08%, the usual chance in the original table
POPULAR_CHANCE = 1500   # 0.15%: equipment of the right level at a popular hunting spot


def rows(name):
    with io.open(os.path.join(REF, name), encoding="utf-8") as f:
        head = f.readline().rstrip("\n").split("\t")
        return [dict(zip(head, line.rstrip("\n").split("\t"))) for line in f]


def sql(statement, fetch=True):
    out = subprocess.run([os.path.join(MYSQL, "mysql"), MYINI, "cosmic", "-N", "-e", statement], capture_output=True, text=True)
    if out.returncode:
        raise SystemExit("Database error (is it running?):\n" + out.stderr[:500])
    return [line.split("\t") for line in out.stdout.splitlines()] if fetch else None


def plan():
    equips = {int(r["id"]): r for r in rows("Equips.tsv") if r["cash"] != "cash" and r["req_level"].isdigit()}
    mobs = {int(r["id"]): r for r in rows("Mobs.tsv") if r["level"].isdigit()}
    spawns = collections.Counter()
    for r in rows("MobSpawns.tsv"):
        if r["count"].isdigit() and r["map_id"].isdigit() and int(r["map_id"]) < 900000000:
            spawns[int(r["mob_id"])] = max(spawns[int(r["mob_id"])], int(r["count"]))
    ordinary = {i for i, m in mobs.items() if not m["boss"] and i < 9000000 and int(m["exp"] or 0) > 0}
    crowded = {i for i in ordinary if spawns[i] >= MIN_SPAWNS}
    names = collections.defaultdict(list)
    for i in crowded:
        names[mobs[i]["name"].lower()].append(i)
    popular = set()
    for r in rows("Hunting-Spots.tsv"):
        found = names.get(r["monster"].lower())
        if found:
            popular.add(max(found, key=lambda i: spawns[i]))
    level = lambda i: int(mobs[i]["level"])

    table = [(int(a), int(b), int(c), int(d)) for a, b, c, d in
             sql("SELECT id, dropperid, itemid, chance FROM drop_data WHERE questid = 0 AND itemid >= 1000000 AND itemid < 2000000")]
    by_item = collections.defaultdict(list)
    per_mob = collections.Counter()
    for row_id, mob, item, chance in table:
        if item in equips and mob in ordinary:
            by_item[item].append((row_id, mob, chance))
        if item in equips:
            per_mob[mob] += 1

    delete, insert, raise_chance = [], [], []
    for item in sorted(by_item):
        need = int(equips[item]["req_level"])
        if not 10 <= need <= 120:
            continue
        keeps = []
        for row_id, mob, chance in by_item[item]:
            gap = level(mob) - need
            if gap > TOO_HIGH or gap < -TOO_LOW:
                delete.append(row_id)
                per_mob[mob] -= 1
            else:
                keeps.append((row_id, mob, chance))
        in_band = lambda mob: need - BAND_BELOW <= level(mob) <= need + BAND_ABOVE
        have = {mob for _, mob, _ in keeps}
        for row_id, mob, chance in keeps:
            if mob in popular and in_band(mob) and chance < POPULAR_CHANCE:
                raise_chance.append(row_id)
        missing = WANTED - sum(1 for mob in have if in_band(mob))
        if missing > 0:
            choice = [m for m in crowded if in_band(m) and m not in have and per_mob[m] < MAX_PER_MONSTER]
            # Popular hunting spots first, then the monsters with the fewest equipment drops; the item's number
            # breaks ties, so that the same run always gives the same answer
            choice.sort(key=lambda m: (m not in popular, per_mob[m], (m * 31 + item) % 97, m))
            for mob in choice[:missing]:
                insert.append((mob, item, POPULAR_CHANCE if mob in popular else NEW_CHANCE))
                per_mob[mob] += 1
    return delete, insert, raise_chance, equips, mobs, popular


def main():
    p = argparse.ArgumentParser(description="Equipment drops from monsters around its level")
    p.add_argument("--check", action="store_true")
    a = p.parse_args()
    delete, insert, raise_chance, equips, mobs, popular = plan()
    print(f"Popular hunting monsters found: {len(popular)}")
    print(f"Drops removed (monster too far above or below the item): {len(delete)}")
    print(f"Drops added (item had fewer than {WANTED} monsters around its level): {len(insert)}, "
          f"{sum(1 for m, _, _ in insert if m in popular)} of them at popular spots")
    print(f"Drops raised to {POPULAR_CHANCE / 10000:.2f}% at popular spots: {len(raise_chance)}")
    for mob, item, chance in insert[:6]:
        print(f"   e.g. {equips[item]['name']} (level {equips[item]['req_level']}) now also from {mobs[mob]['name']} (level {mobs[mob]['level']})")
    if a.check or not (delete or insert or raise_chance):
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
    for i in range(0, len(raise_chance), 500):
        statements.append(f"UPDATE drop_data SET chance = {POPULAR_CHANCE} WHERE id IN (" + ",".join(map(str, raise_chance[i:i + 500])) + ")")
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
