"""Estimates what a solo player earns and spends on the way from level 1 to 120.

    python Settings/Scripts/Simulate-Economy.py                 the table per ten levels
    python Settings/Scripts/Simulate-Economy.py --levels        one row per level
    python Settings/Scripts/Simulate-Economy.py --meso-rate 3   try other rates than the ones in config.yaml
    python Settings/Scripts/Simulate-Economy.py --potion-price 0.5   potions at half price
    python Settings/Scripts/Simulate-Economy.py --equip-sell 0.25    vendors pay a quarter for equipment

The database must be running (it holds the drop tables). Nothing is changed.

What is real data: experience needed per level, each monster's level, experience and touch damage, what it
drops and how often, what a vendor pays for each item, what potions and gear cost in shops, and the rates
in Settings/config.yaml.

What is assumed is in the block below. Change the numbers there to try other assumptions.
"""
import argparse
import collections
import glob
import io
import os
import re
import subprocess
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(os.path.dirname(HERE))
REF = os.path.join(ROOT, "Settings", "Reference")
WZ = os.path.join(ROOT, "Server", "wz")

# ---------------------------------------------------------------------------------------------
# Assumptions
# ---------------------------------------------------------------------------------------------
LEVELS_BELOW = 7            # a player trains on monsters from this many levels below their own...
LEVELS_ABOVE = 1            # ...to this many above
MIN_SPAWNS = 8              # only monsters with at least this many in one map count as training monsters
PICKED_UP = 0.8             # share of the dropped mesos and items the player actually picks up and sells
NATURAL_RECOVERY = 0.2      # share of the lost HP and MP that comes back by itself (resting, level-ups)
SKILL_USES_PER_KILL = 2.5   # attacks needed for a monster of about the player's level

# Three kinds of player. hits: how often a monster touches them per kill, as a share of its touch damage
# that gets through. mp: MP per skill use at (from level, MP) steps. targets: monsters hit per skill use.
PLAYERS = {
    "warrior": {"line": "hero", "hits": 1.2, "taken": 0.75,
                "mp": [(1, 0), (10, 8), (30, 12), (70, 18)], "targets": [(1, 1), (30, 1.5), (70, 3)]},
    "mage": {"line": "fp", "hits": 0.5, "taken": 0.9,
             "mp": [(1, 0), (8, 14), (30, 26), (70, 45)], "targets": [(1, 1), (30, 1.5), (70, 4)]},
    "thief": {"line": "assassin", "hits": 0.5, "taken": 0.85,
              "mp": [(1, 0), (10, 10), (30, 16), (70, 22)], "targets": [(1, 1), (70, 2)]},
}
HP_POTIONS = [2000000, 2000001, 2000002, 2022003, 2001001, 2001002]     # Red, Orange, White, Unagi, Ice Cream Pop, Sundae
MP_POTIONS = [2000003, 2000006, 2022000, 2001000]                         # Blue, Mana Elixir, Pure Water, Watermelon


def rows(name):
    with io.open(os.path.join(REF, name), encoding="utf-8") as f:
        head = f.readline().rstrip("\n").split("\t")
        for line in f:
            yield dict(zip(head, line.rstrip("\n").split("\t")))


def step(steps, level):
    value = steps[0][1]
    for start, v in steps:
        if level >= start:
            value = v
    return value


def config_rate(name):
    with io.open(os.path.join(ROOT, "Settings", "config.yaml"), encoding="utf-8") as f:
        m = re.search(r"^\s*" + name + r":\s*(\d+)", f.read(), re.M)
    return int(m.group(1)) if m else 1


def exp_table():
    path = os.path.join(ROOT, "Server", "src", "main", "java", "constants", "game", "ExpTable.java")
    with io.open(path, encoding="utf-8") as f:
        m = re.search(r"int\[\] exp = \{([^}]*)\}", f.read())
    return [int(x) for x in m.group(1).split(",")]


def sell_prices():
    """What a vendor pays for each item: the price in the item data."""
    prices = {}
    entry = re.compile(r'<imgdir name="0?(\d{7})">(.*?)<int name="price" value="(\d+)"', re.S)
    for path in glob.glob(os.path.join(WZ, "Item.wz", "*", "*.img.xml")):
        with io.open(path, encoding="utf-8", errors="ignore") as f:
            text = f.read()
        for block in re.split(r'(?=<imgdir name="0?\d{7}">)', text):
            m = re.match(r'<imgdir name="0?(\d{7})">', block)
            p = re.search(r'<int name="price" value="(\d+)"', block)
            if m and p:
                prices[int(m.group(1))] = int(p.group(1))
    for path in glob.glob(os.path.join(WZ, "Character.wz", "*", "*.img.xml")):
        m = re.match(r"0?(\d{7})\.img\.xml", os.path.basename(path))
        if not m:
            continue
        with io.open(path, encoding="utf-8", errors="ignore") as f:
            p = re.search(r'<int name="price" value="(\d+)"', f.read(20000))
        if p:
            prices[int(m.group(1))] = int(p.group(1))
    return prices


def touch_damage(mob_id):
    path = os.path.join(WZ, "Mob.wz", f"{int(mob_id):07d}.img.xml")
    if not os.path.exists(path):
        return 0
    with io.open(path, encoding="utf-8", errors="ignore") as f:
        m = re.search(r'<int name="PADamage" value="(\d+)"', f.read(4000))
    return int(m.group(1)) if m else 0


def drop_table():
    mysql = os.path.join(ROOT, "Tools", "mysql", "bin", "mysql")
    out = subprocess.run([mysql, "--defaults-file=" + os.path.join(ROOT, "Settings", "mysql.ini"), "cosmic", "-N", "-e",
                          "SELECT dropperid,itemid,minimum_quantity,maximum_quantity,questid,chance FROM drop_data"],
                         capture_output=True, text=True)
    if out.returncode:
        raise SystemExit("Could not read the drop table. Is the database running?\n" + out.stderr)
    drops = collections.defaultdict(list)
    for line in out.stdout.splitlines():
        mob, item, low, high, quest, chance = (int(x) for x in line.split("\t"))
        drops[mob].append((item, low, high, quest, chance))
    return drops


def main():
    p = argparse.ArgumentParser(description="Estimate earnings and costs per level")
    p.add_argument("--levels", action="store_true", help="one row per level instead of per ten levels")
    p.add_argument("--exp-rate", type=float)
    p.add_argument("--meso-rate", type=float)
    p.add_argument("--drop-rate", type=float)
    p.add_argument("--potion-price", type=float, default=1.0, help="multiply potion shop prices by this")
    p.add_argument("--early-meso", type=float, default=1.0, help="multiply mesos dropped by monsters under level 30 by this")
    p.add_argument("--equip-sell", type=float, default=1.0, help="multiply what vendors pay for equipment by this")
    p.add_argument("--to", type=int, default=120)
    a = p.parse_args()
    exp_rate = a.exp_rate or config_rate("exp_rate")
    meso_rate = a.meso_rate or config_rate("meso_rate")
    drop_rate = a.drop_rate or config_rate("drop_rate")

    need = exp_table()
    prices = sell_prices()
    drops = drop_table()
    spawns = collections.Counter()
    for r in rows("MobSpawns.tsv"):
        if r["count"].isdigit():
            spawns[r["mob_id"]] = max(spawns[r["mob_id"]], int(r["count"]))
    shop_price = {}
    for r in rows("Shops.tsv"):
        if r["price_meso"].isdigit() and int(r["price_meso"]) > 0:
            item = int(r["item_id"])
            shop_price[item] = min(shop_price.get(item, 10 ** 12), int(r["price_meso"]))
    heals = {}
    for r in rows("Items.tsv"):
        m_hp = re.search(r"Recovers (?:around )?(\d+) HP", r["description"])
        m_mp = re.search(r"Recovers (?:around )?(\d+) MP", r["description"])
        heals[int(r["id"])] = (int(m_hp.group(1)) if m_hp else 0, int(m_mp.group(1)) if m_mp else 0)
    hp_cost = min(shop_price[i] / heals[i][0] for i in HP_POTIONS if i in shop_price and heals.get(i, (0, 0))[0]) * a.potion_price
    mp_cost = min(shop_price[i] / heals[i][1] for i in MP_POTIONS if i in shop_price and heals.get(i, (0, 0))[1]) * a.potion_price

    # What one kill of each training monster is worth
    mobs = []
    for r in rows("Mobs.tsv"):
        if not (r["level"].isdigit() and r["exp"].isdigit()) or r["boss"] or int(r["exp"]) <= 0:
            continue
        if spawns[r["id"]] < MIN_SPAWNS or int(r["id"]) not in drops:
            continue
        early = a.early_meso if int(r["level"]) < 30 else 1.0
        meso = items = 0.0
        for item, low, high, quest, chance in drops[int(r["id"])]:
            odds = min(1.0, chance / 1000000 * drop_rate)
            amount = (low + high) / 2
            if item == 0:
                meso += odds * amount * meso_rate * early
            elif not quest:
                items += odds * amount * prices.get(item, 0) * (a.equip_sell if item < 2000000 else 1.0)
        mobs.append({"level": int(r["level"]), "exp": int(r["exp"]), "meso": meso, "items": items,
                     "touch": touch_damage(r["id"]), "name": r["name"]})

    gear = {}
    for name, kind in PLAYERS.items():
        owned, by_level = set(), collections.defaultdict(float)
        for r in rows("Loadouts.tsv"):
            if r["line"] == kind["line"] and r["gender"] in ("m", "", "all") and r["item_id"].isdigit():
                item = int(r["item_id"])
                if item not in owned:
                    owned.add(item)
                    by_level[int(r["level"])] += shop_price.get(item, 0)
        gear[name] = by_level

    table, purse = [], {name: 0.0 for name in PLAYERS}
    for level in range(1, a.to):
        fits = [m for m in mobs if max(1, level - LEVELS_BELOW) <= m["level"] <= level + LEVELS_ABOVE]
        if not fits:
            continue
        avg = lambda key: sum(m[key] for m in fits) / len(fits)
        kills = need[level - 1] / (avg("exp") * exp_rate)
        row = {"level": level, "kills": kills, "meso": kills * avg("meso") * PICKED_UP,
               "items": kills * avg("items") * PICKED_UP}
        for name, kind in PLAYERS.items():
            targets = step(kind["targets"], level)
            hp = kills * avg("touch") * kind["hits"] * kind["taken"] * (1 - NATURAL_RECOVERY)
            mp = kills * SKILL_USES_PER_KILL / targets * step(kind["mp"], level) * (1 - NATURAL_RECOVERY)
            row[name + "_pots"] = hp * hp_cost + mp * mp_cost
            row[name + "_gear"] = gear[name].get(level, 0)
            purse[name] += row["meso"] + row["items"] - row[name + "_pots"] - row[name + "_gear"]
            row[name + "_purse"] = purse[name]
        table.append(row)

    print(f"Rates: exp x{exp_rate:g}, meso x{meso_rate:g}, drop x{drop_rate:g}. "
          f"Potions cost {hp_cost:.2f} mesos per HP and {mp_cost:.2f} per MP.")
    print("Mesos per level band. 'left' is income minus potions and shop gear; 'purse' is the running total.\n")
    head = f"{'levels':>8} {'kills':>8} {'mesos':>10} {'vendor':>10} |"
    for name in PLAYERS:
        head += f" {name + ' pots':>13} {'gear':>9} {'left':>10} {'purse':>11} |"
    print(head)
    size = 1 if a.levels else 10
    for start in range(1, a.to, size):
        part = [r for r in table if start <= r["level"] < start + size]
        if not part:
            continue
        total = lambda key: sum(r[key] for r in part)
        label = str(start) if a.levels else f"{start}-{min(start + size - 1, a.to)}"
        line = f"{label:>8} {total('kills'):>8,.0f} {total('meso'):>10,.0f} {total('items'):>10,.0f} |"
        for name in PLAYERS:
            left = total("meso") + total("items") - total(name + "_pots") - total(name + "_gear")
            line += (f" {total(name + '_pots'):>13,.0f} {total(name + '_gear'):>9,.0f} {left:>10,.0f} "
                     f"{part[-1][name + '_purse']:>11,.0f} |")
        print(line)


if __name__ == "__main__":
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")
    main()
