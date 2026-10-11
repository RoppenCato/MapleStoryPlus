"""Applies our price and meso changes to the database. Each change is applied once.

    python Settings/Scripts/Apply-Economy-Changes.py            apply what has not been applied yet
    python Settings/Scripts/Apply-Economy-Changes.py --check    show what would be done, change nothing

The database must be running and the game server stopped (it reads shops and drops when it needs them and
keeps them). A backup is saved to Backups/ before anything is changed.

Which changes have been applied is remembered in the table plus_changes, so running this again does nothing.
To add a change, add a function with the @change decorator below; never edit one that has been applied.
"""
import argparse
import datetime
import io
import os
import subprocess
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(os.path.dirname(HERE))
MYSQL = os.path.join(ROOT, "Tools", "mysql", "bin")
MYINI = "--defaults-file=" + os.path.join(ROOT, "Settings", "mysql.ini")
CHANGES = []


def sql(statement):
    out = subprocess.run([os.path.join(MYSQL, "mysql"), MYINI, "cosmic", "-N", "-e", statement],
                         capture_output=True, text=True)
    if out.returncode:
        raise SystemExit("Database error (is it running?):\n" + out.stderr)
    return [line.split("\t") for line in out.stdout.splitlines()]


def change(name, why):
    def register(function):
        CHANGES.append((name, why, function))
        return function
    return register


def mob_levels():
    levels = {}
    with io.open(os.path.join(ROOT, "Settings", "Reference", "Mobs.tsv"), encoding="utf-8") as f:
        f.readline()
        for line in f:
            cells = line.split("\t")
            if cells[2].isdigit():
                levels[int(cells[0])] = int(cells[2])
    return levels


@change("2026-10-11 basic potions half price",
        "Potions cost more than monsters paid during the first 30 levels (Simulate-Economy.py).")
def basic_potions_half_price():
    # Red, Orange, White and Blue Potion, Mana Elixir. Never below what a vendor pays for one, or buying
    # and selling them back would make money.
    sells_for = {2000000: 25, 2000001: 80, 2000002: 160, 2000003: 100, 2000006: 310}
    statements = [f"UPDATE shopitems SET price = GREATEST({floor}, CEIL(price / 2)) WHERE itemid = {item} AND price > 0"
                  for item, floor in sells_for.items()]
    return statements, "5 potions in every shop that sells them"


@change("2026-10-11 double mesos under level 30",
        "Same reason: early income should not depend on a lucky equipment drop.")
def early_mesos_doubled():
    early = sorted(mob for mob, level in mob_levels().items() if level < 30)
    ids = ",".join(str(mob) for mob in early)
    return ([f"UPDATE drop_data SET minimum_quantity = minimum_quantity * 2, maximum_quantity = maximum_quantity * 2 "
             f"WHERE itemid = 0 AND dropperid IN ({ids})"], f"meso drops of the {len(early)} monsters under level 30")


def main():
    p = argparse.ArgumentParser(description="Apply price and meso changes to the database")
    p.add_argument("--check", action="store_true")
    a = p.parse_args()
    sql("CREATE TABLE IF NOT EXISTS plus_changes (name VARCHAR(120) PRIMARY KEY, applied_at DATETIME NOT NULL)")
    done = {row[0] for row in sql("SELECT name FROM plus_changes")}
    todo = [c for c in CHANGES if c[0] not in done]
    for name, why, function in CHANGES:
        print(("applied   " if name in done else "to apply  ") + name)
    if not todo or a.check:
        print("Nothing to do." if not todo else "Check only: nothing changed.")
        return
    if sql("SELECT COUNT(*) FROM accounts WHERE loggedin <> 0")[0][0] != "0":
        raise SystemExit("Someone is logged in. Stop the game server first.")
    stamp = datetime.datetime.now().strftime("%Y-%m-%d_%H%M%S")
    backup = os.path.join(ROOT, "Backups", f"cosmic_{stamp}_before-economy.sql")
    os.makedirs(os.path.dirname(backup), exist_ok=True)
    out = subprocess.run([os.path.join(MYSQL, "mysqldump"), MYINI, "--single-transaction", "--routines", "--databases",
                          "cosmic", "--result-file=" + backup], capture_output=True, text=True)
    if out.returncode:
        raise SystemExit("Backup failed, nothing changed:\n" + out.stderr)
    print("Backup: " + backup)
    for name, why, function in todo:
        statements, what = function()
        mark = "INSERT INTO plus_changes VALUES ('" + name + "', NOW())"
        sql("START TRANSACTION; " + "; ".join(statements) + "; " + mark + "; COMMIT")
        print(f"Applied: {name} ({what})")


if __name__ == "__main__":
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")
    main()
