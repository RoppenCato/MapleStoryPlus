"""Writes Settings/Fixed-Shops.tsv: the set shops in the Free Market that always sell what a player needs.

    python Settings/Scripts/Make-Fixed-Shops.py

The server reads that file when it fills the Free Market at start. Rooms listed in it get these shops
instead of random ones; stock never runs out and prices do not move.

Prices and the shop layout are the tables below. Change them here and run this again; do not edit the
.tsv by hand, it is overwritten. A shop holds at most 16 items (the game's limit), so a group with more
is split into "... 1", "... 2".
"""
import collections
import io
import os
import re

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(os.path.dirname(HERE))
REF = os.path.join(ROOT, "Settings", "Reference")
OUT = os.path.join(ROOT, "Settings", "Fixed-Shops.tsv")
PER_SHOP = 16
SPOTS_PER_ROOM = 23             # shop positions in a Henesys-style Free Market room

# Mesos per scroll, by success rate. Dark scrolls (30% and 70%) can destroy the item.
SCROLL_PRICE = {100: 100_000, 60: 300_000, 10: 150_000, 70: 1_000_000, 30: 2_000_000}

# Room 1: weapon and accessory scrolls, special scrolls and supplies. Room 2: armour scrolls.
# One room cannot hold everything: there are about 440 ordinary scrolls and a room has 23 shops of 16 items.
# (title, [scroll groups]); a scroll group is the item id without its last two digits.
WEAPON_SHOPS = [
    ("One-Handed Sword scrolls", [20430]),
    ("One-Handed Axe and Dagger scrolls", [20431, 20433]),
    ("One-Handed BW and Wand scrolls", [20432, 20437]),
    ("Staff, Bow and Crossbow scrolls", [20438, 20445, 20446]),
    ("Two-Handed Sword and Claw scrolls", [20440, 20447]),
    ("Two-Handed Axe and Gun scrolls", [20441, 20449]),
    ("Two-Handed BW scrolls", [20442]),
    ("Spear scrolls", [20443]),
    ("Pole Arm scrolls", [20444]),
    ("Knuckler scrolls", [20448]),
]
ARMOUR_SHOPS = [
    ("Helmet scrolls", [20400]),
    ("Topwear scrolls", [20404]),
    ("Bottomwear scrolls", [20406]),
    ("Overall scrolls", [20405]),
    ("Shoes scrolls", [20407]),
    ("Gloves scrolls", [20408]),
    ("Shield scrolls", [20409]),
    ("Cape scrolls", [20410]),
    ("Pet Equip scrolls", [20480]),
]
ACCESSORY_SHOPS = [
    ("Earring scrolls", [20403]),
    ("Face and Eye Accessory scrolls", [20401, 20402]),
    ("Ring scrolls", [20411]),
    ("Belt scrolls", [20413]),
    ("Accessory dark scrolls", [20492]),
]
# (title, [(item id, price)]). Throwing stars, bullets and capsules are sold as one full set.
OTHER_SHOPS = [
    ("Special scrolls", [(2049000, 250_000), (2049001, 500_000), (2049002, 1_000_000), (2049003, 3_000_000),
                         (2049100, 10_000_000), (2340000, 25_000_000)]),
    ("Potions", [(2000004, 4_000), (2000005, 10_000), (2050004, 1_500), (2002006, 500), (2002007, 500),
                 (2002008, 500), (2002009, 500), (2002010, 475), (2002018, 5_000)]),
    # The best stars and bullets (Steely, Ilbi, Hwabi; Shiny, Eternal) are left out on purpose: they are drops.
    ("Stars, bullets and capsules", [(2070001, 30_000), (2070002, 100_000), (2070003, 400_000), (2070004, 1_500_000),
                                     (2330001, 30_000), (2330002, 100_000), (2330003, 400_000),
                                     (2331000, 2_000), (2332000, 2_000)]),
    ("Gear for scrolling", [(1082002, 150_000), (1102053, 500_000), (1102054, 300_000), (1102041, 1_500_000),
                            (1102040, 2_000_000), (1050100, 300_000), (1051098, 300_000), (1032013, 300_000),
                            (1092008, 50_000), (1092030, 1_000_000)]),
]


def rows(name):
    with io.open(os.path.join(REF, name), encoding="utf-8") as f:
        head = f.readline().rstrip("\n").split("\t")
        return [dict(zip(head, line.rstrip("\n").split("\t"))) for line in f]


def strength(stats):
    """All the bonuses of a scroll added up, to compare two scrolls of one kind."""
    return sum(int(n) for n in re.findall(r"\+(\d+)", stats))


def scrolls_by_group():
    """The ordinary scrolls: 10%, 60%, 100% and the dark 30% and 70%. Event scrolls and GM scrolls are left out."""
    families = collections.defaultdict(list)
    for r in rows("Scrolls.tsv"):
        if not r["id"].startswith("204") or re.search(r"\[|King Pepe|Anniv", r["name"]) or r["other"]:
            continue
        rate, destroys = r["success_percent"], r["destroy_percent"]
        if not ((rate in ("10", "60", "100") and not destroys) or (rate in ("30", "70") and destroys)):
            continue
        root = re.sub(r"\s*\d+%\s*$", "", r["name"].strip())
        root = re.sub(r"^dark\s+", "", root, flags=re.I).lower().replace("rings", "ring")
        families[(int(r["id"]) // 100, root)].append(r)
    groups = collections.defaultdict(list)
    for (group, root), members in sorted(families.items(), key=lambda kv: min(int(r["id"]) for r in kv[1])):
        sixty = [strength(r["stats"]) for r in members if r["success_percent"] == "60"]
        for r in sorted(members, key=lambda r: (-int(r["success_percent"]) if not r["destroy_percent"] else 1000 - int(r["success_percent"]))):
            # A 100% scroll as strong as the 60% one is a GM scroll
            if r["success_percent"] == "100" and sixty and strength(r["stats"]) >= max(sixty):
                continue
            rate = int(r["success_percent"])
            name = r["name"].strip()
            if not re.search(r"\d+%", name):
                name += f" {rate}%"
            groups[group].append((int(r["id"]), name + (f" ({r['stats']})" if r["stats"] else ""), SCROLL_PRICE[rate]))
    return groups


def main():
    names = {int(r["id"]): r["name"] for r in rows("Items.tsv")}
    names.update({int(r["id"]): r["name"] for r in rows("Equips.tsv")})
    groups = scrolls_by_group()

    def scroll_shops(layout):
        shops = []
        for title, ids in layout:
            items = [item for group in ids for item in groups.get(group, [])]
            parts = [items[i:i + PER_SHOP] for i in range(0, len(items), PER_SHOP)]
            for number, part in enumerate(parts, 1):
                shops.append((title if len(parts) == 1 else f"{title} {number}", part))
        return shops

    others = [(title, [(item, names.get(item, "?"), price) for item, price in items]) for title, items in OTHER_SHOPS]
    rooms = {910000001: scroll_shops(WEAPON_SHOPS) + others + scroll_shops(ACCESSORY_SHOPS),
             910000002: scroll_shops(ARMOUR_SHOPS)}
    lines = ["room\tspot\ttitle\titem_id\titem\tprice"]
    for room, shops in rooms.items():
        if len(shops) > SPOTS_PER_ROOM:
            raise SystemExit(f"Room {room} has {len(shops)} shops but only {SPOTS_PER_ROOM} spots.")
        for spot, (title, items) in enumerate(shops):
            for item, name, price in items:
                if name == "?":
                    raise SystemExit(f"Unknown item {item} in shop '{title}'.")
                lines.append(f"{room}\t{spot}\t{title}\t{item}\t{name}\t{price}")
        print(f"Room {room % 100}: {len(shops)} shops, {sum(len(items) for _, items in shops)} items")
    with io.open(OUT, "w", encoding="utf-8", newline="\n") as f:
        f.write("\n".join(lines) + "\n")
    print("Wrote " + OUT)


if __name__ == "__main__":
    main()
