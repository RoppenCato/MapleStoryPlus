"""Writes Settings/Boss-Gear.tsv: the gear the trial bosses roll their two guaranteed pieces from.

    python Settings/Reference/Build-Reference.py      first, so the lists match the database
    python Settings/Scripts/Make-Boss-Gear.py

Run it after Rebalance-Drops.py, because the list is taken from the drop table: every weapon and piece
of armour that an ordinary monster drops. So whatever counts as ordinary gear for monsters is what
bosses roll on, and event items stay out. The server reads the file when the first boss dies after a
start; which level a boss rolls on is the gear_level column of Settings/Trials.tsv.
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
    with io.open(os.path.join(ROOT, "Settings", "Boss-Gear.tsv"), "w", encoding="utf-8", newline="\n") as f:
        f.write("\n".join(lines) + "\n")
    print(f"{len(lines) - 1} items written to Settings/Boss-Gear.tsv")


if __name__ == "__main__":
    main()
