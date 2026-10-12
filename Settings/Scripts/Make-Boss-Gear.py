"""Writes Settings/Boss-Gear.tsv: the gear the trial bosses roll their two guaranteed pieces from.

    python Settings/Reference/Build-Reference.py      first, so the lists match the database
    python Settings/Scripts/Make-Boss-Gear.py

Run it after Rebalance-Drops.py, because the list is taken from the drop table: every weapon and piece
of armour that an ordinary monster drops. So whatever counts as ordinary gear for monsters is what
bosses roll on, and event items stay out.

Two tiers above that are boss loot only and are added here by name and level:
  level 110   the Dragon weapons and the class sets of that level (Blue Dragon, Garina, Canopus, Red Hunter ...)
  level 120   the Reverse and Timeless weapons and armour

The server reads the file when the first boss dies after a start; which level a boss rolls on is the
gear_level column of Settings/Trials.tsv.
"""
import io
import os

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(os.path.dirname(HERE))
REF = os.path.join(ROOT, "Settings", "Reference")
ARMOUR = ("Cap", "Coat", "Longcoat", "Pants", "Shoes", "Glove", "Shield", "Cape", "Accessory")


def rows(name):
    with io.open(os.path.join(REF, name), encoding="utf-8") as f:
        head = f.readline().rstrip("\n").split("\t")
        return [dict(zip(head, line.rstrip("\n").split("\t"))) for line in f]


def main():
    equips = {r["id"]: r for r in rows("Equips.tsv") if r["cash"] != "cash" and r["req_level"].isdigit()}
    mobs = {r["id"]: r for r in rows("Mobs.tsv")}
    dropped = set()
    for d in rows("Drops.tsv"):
        mob = mobs.get(d["mob_id"])
        if d["item_id"] in equips and mob and not mob["boss"] and int(d["mob_id"]) < 9000000 and d["quest_id"] in ("", "0"):
            dropped.add(d["item_id"])
    lines = ["item_id\titem\treq_level\tclasses\tkind"]
    for item in sorted(dropped, key=lambda i: (int(equips[i]["req_level"]), int(i))):
        e = equips[item]
        if e["type"] != "Weapon" and e["type"] not in ARMOUR:
            continue
        if not 8 <= int(e["req_level"]) <= 120:
            continue
        classes = "warrior/magician/bowman/thief/pirate" if e["job"] == "all" else e["job"]
        lines.append(f"{item}\t{e['name']}\t{e['req_level']}\t{classes}\t{'weapon' if e['type'] == 'Weapon' else 'armour'}")
    listed = {line.split("\t")[0] for line in lines[1:]}
    tiers = 0
    for item, e in sorted(equips.items(), key=lambda kv: (int(kv[1]["req_level"]), int(kv[0]))):
        level = int(e["req_level"])
        dragon = 108 <= level <= 110
        timeless = 118 <= level <= 120 and (e["name"].startswith("Reverse ") or e["name"].startswith("Timeless "))
        if item in listed or not (dragon or timeless) or (e["type"] != "Weapon" and e["type"] not in ARMOUR) or e["type"] == "Accessory":
            continue
        if not e["name"].strip() or e["name"].startswith("MISSING") or e["job"] == "all":
            continue
        lines.append(f"{item}\t{e['name']}\t{e['req_level']}\t{e['job']}\t{'weapon' if e['type'] == 'Weapon' else 'armour'}")
        tiers += 1
    print(f"{tiers} of them are the level 110 and level 120 boss tiers")
    with io.open(os.path.join(ROOT, "Settings", "Boss-Gear.tsv"), "w", encoding="utf-8", newline="\n") as f:
        f.write("\n".join(lines) + "\n")
    print(f"{len(lines) - 1} items written to Settings/Boss-Gear.tsv")


if __name__ == "__main__":
    main()
