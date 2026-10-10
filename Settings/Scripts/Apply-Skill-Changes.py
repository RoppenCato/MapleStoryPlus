"""Applies the skill changes listed in Skill-Changes.tsv to the server's skill data (Server/wz/Skill.wz).

    python Settings/Scripts/Apply-Skill-Changes.py            apply
    python Settings/Scripts/Apply-Skill-Changes.py --check    show what would change, write nothing
    python Settings/Scripts/Apply-Skill-Changes.py --export FILE   list the current server values, for the client patcher

Each row sets one field of one skill at every level. The value is a small formula in L (the skill
level), M (the skill's max level) and V (the value the field has now), for example  90*L  or  10  or
max(V, 1800*L//M). Running the script twice changes nothing the second time.

The server must be restarted to pick up the changes. The client has its own copy of this data; a
change the client also needs (damage, hit count, number of targets) will not show until that copy is
edited too. Buff durations, speed and cooldowns are sent by the server.
"""
import io
import os
import re
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(os.path.dirname(HERE))
SKILL_WZ = os.path.join(ROOT, "Server", "wz", "Skill.wz")
CHANGES = os.path.join(HERE, "Skill-Changes.tsv")

LEVEL_BLOCK = re.compile(r'(?P<indent>[ \t]*)<imgdir name="(?P<level>\d+)">\r?\n(?P<body>.*?)(?P=indent)</imgdir>', re.S)


def load_changes():
    with io.open(CHANGES, encoding="utf-8") as f:
        rows = [line.rstrip("\n").split("\t") for line in f if line.strip() and not line.startswith("#")]
    header = rows[0]
    return [dict(zip(header, r + [""] * (len(header) - len(r)))) for r in rows[1:]]


def skill_span(text, skill_id):
    """(start, end) of the skill's <imgdir name="level"> block."""
    start = text.find(f'<imgdir name="{skill_id:07d}">')
    if start < 0:
        return None
    level_start = text.find('<imgdir name="level">', start)
    next_skill = re.search(r'\n    <imgdir name="\d{7}">', text[start + 10:])
    limit = start + 10 + next_skill.start() if next_skill else len(text)
    if level_start < 0 or level_start > limit:
        return None
    indent = text[text.rfind("\n", 0, level_start) + 1:level_start]
    end = text.find("\n" + indent + "</imgdir>", level_start)
    return level_start, end


def apply_change(text, skill_id, field, formula):
    """Returns (new text, levels changed)."""
    span = skill_span(text, skill_id)
    if not span:
        raise SystemExit(f"Skill {skill_id}: not found in the server data")
    start, end = span
    block = text[start:end]
    levels = [int(m.group("level")) for m in LEVEL_BLOCK.finditer(block)]
    top = max(levels)
    changed = 0

    def edit(m):
        nonlocal changed
        level = int(m.group("level"))
        body = m.group("body")
        existing = re.search(rf'<int name="{field}" value="(-?\d+)"/>', body)
        current = int(existing.group(1)) if existing else 0
        value = int(eval(formula, {"__builtins__": {}},
                         {"L": level, "M": top, "V": current, "min": min, "max": max, "round": round}))
        if existing:
            if int(existing.group(1)) == value:
                return m.group(0)
            body = body[:existing.start()] + f'<int name="{field}" value="{value}"/>' + body[existing.end():]
        else:
            newline = "\r\n" if "\r\n" in m.group(0) else "\n"
            body = f'{m.group("indent")}  <int name="{field}" value="{value}"/>{newline}' + body
        changed += 1
        head = m.group(0)[:m.group(0).index(m.group("body"))]
        return head + body + m.group("indent") + "</imgdir>"

    return text[:start] + LEVEL_BLOCK.sub(edit, block) + text[end:], changed


def export(path):
    """Writes the value every listed field has in the server data now, one row per skill level.
    The client patcher uses this to make the client's copy match the server's."""
    seen = set()
    rows = ["skill_id\tlevel\tfield\tvalue"]
    texts = {}
    for row in load_changes():
        skill_id, field = int(row["skill_id"]), row["field"]
        if (skill_id, field) in seen:
            continue
        seen.add((skill_id, field))
        file = os.path.join(SKILL_WZ, "%03d.img.xml" % (skill_id // 10000))
        if file not in texts:
            with io.open(file, encoding="utf-8", newline="") as f:
                texts[file] = f.read()
        start, end = skill_span(texts[file], skill_id)
        for m in LEVEL_BLOCK.finditer(texts[file][start:end]):
            value = re.search(rf'<int name="{field}" value="(-?\d+)"/>', m.group("body"))
            if value:
                rows.append(f"{skill_id}\t{m.group('level')}\t{field}\t{value.group(1)}")
    with io.open(path, "w", encoding="utf-8", newline="\n") as f:
        f.write("\n".join(rows) + "\n")
    print(f"Exported {len(rows) - 1} values to {path}")


def main():
    if "--export" in sys.argv:
        export(sys.argv[sys.argv.index("--export") + 1])
        return
    check = "--check" in sys.argv
    files = {}
    total = 0
    for row in load_changes():
        skill_id = int(row["skill_id"])
        path = os.path.join(SKILL_WZ, "%03d.img.xml" % (skill_id // 10000))
        if path not in files:
            with io.open(path, encoding="utf-8", newline="") as f:
                files[path] = [f.read(), False]
        new, changed = apply_change(files[path][0], skill_id, row["field"], row["value"])
        if changed:
            files[path] = [new, True]
            total += changed
        print(f'{row["skill"]:28} {row["field"]:9} = {row["value"]:24} {"changed " + str(changed) + " levels" if changed else "already set"}')
    if not check:
        for path, (text, dirty) in files.items():
            if dirty:
                with io.open(path, "w", encoding="utf-8", newline="") as f:
                    f.write(text)
    print(("Would change" if check else "Changed") + f" {total} values." + ("" if check else " Restart the server to load them."))


if __name__ == "__main__":
    main()
