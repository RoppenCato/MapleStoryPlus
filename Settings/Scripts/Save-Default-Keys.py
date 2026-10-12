"""Makes one character's key bindings the ones every new character starts with.

    python Settings/Scripts/Save-Default-Keys.py Shym

Log the character out first: the game only saves key bindings to the database when the character
leaves the game. Writes Settings/Default-Keys.tsv, which the server reads for every new character
(plus/DefaultKeys.java), so no restart is needed. Delete the file to go back to the game's own keys.

What is saved:
  * every key that opens a window or does an action (attack, pick up, jump, sit, chat ...)
  * beginner skills on keys (Nimble Feet, Recovery, Three Snails), which every new character has
  * the eight quick slots, which a new account gets with its first character
Not saved: job skills and potions on keys, which a new character does not have.
"""
import io
import os
import struct
import subprocess
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(os.path.dirname(HERE))
MYSQL = os.path.join(ROOT, "Tools", "mysql", "bin", "mysql.exe")
INI = os.path.join(ROOT, "Settings", "mysql.ini")
SKILL = 1
BEGINNER_SKILLS_BELOW = 10000       # 1000 Three Snails, 1001 Recovery, 1002 Nimble Feet
KINDS = {1: "skill", 4: "window or action", 5: "action", 6: "expression"}


def sql(query):
    out = subprocess.run([MYSQL, "--defaults-file=" + INI, "cosmic", "-N", "-B", "-e", query],
                         capture_output=True, text=True, encoding="utf-8")
    if out.returncode:
        sys.exit(out.stderr.strip())
    return [line.split("\t") for line in out.stdout.splitlines() if line.strip()]


def main():
    if len(sys.argv) != 2 or not sys.argv[1].isalnum():
        sys.exit(__doc__)
    found = sql(f"SELECT c.id, c.accountid, a.loggedin FROM characters c JOIN accounts a ON a.id = c.accountid WHERE c.name = '{sys.argv[1]}'")
    if not found:
        sys.exit(f"No character is called {sys.argv[1]}.")
    cid, account, logged_in = found[0]
    if logged_in != "0":
        sys.exit(f"{sys.argv[1]}'s account is in the game. Log out first, or the keys in the database are the old ones.")
    lines = ["key\ttype\taction\tkind"]
    left_out = 0
    for key, kind, action in sql(f"SELECT `key`, `type`, `action` FROM keymap WHERE characterid = {cid} ORDER BY `key`"):
        kind, action = int(kind), int(action)
        if kind in (4, 5, 6) or (kind == SKILL and action < BEGINNER_SKILLS_BELOW):
            lines.append(f"{key}\t{kind}\t{action}\t{KINDS[kind]}")
        elif kind != 0:
            left_out += 1
    slots = sql(f"SELECT keymap FROM quickslotkeymapped WHERE accountid = {account}")
    if slots:
        # The server packs the eight key numbers into one number (tools/LongTool.java)
        keys = struct.pack(">q", int(slots[0][0]))
        lines.append("quickslots\t" + "\t".join(str(b) for b in keys))
    with io.open(os.path.join(ROOT, "Settings", "Default-Keys.tsv"), "w", encoding="utf-8", newline="\n") as f:
        f.write("\n".join(lines) + "\n")
    print(f"{len(lines) - 1 - bool(slots)} keys saved from {sys.argv[1]}" + (", and the quick slots" if slots else ", no quick slots of its own")
          + (f"; {left_out} job skills or items on keys left out" if left_out else "") + ". New characters start with them.")


if __name__ == "__main__":
    main()
