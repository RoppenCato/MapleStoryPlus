"""Rebuilds the ID reference lists in this folder from the server's game data (Server/wz).

Run again after editing the game data:  python Settings/Reference/Build-Reference.py
"""
import glob
import html
import os
import re
import subprocess
import xml.etree.ElementTree as ET

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(os.path.dirname(HERE))
WZ = os.path.join(ROOT, "Server", "wz")
JOB_JAVA = os.path.join(ROOT, "Server", "src", "main", "java", "client", "Job.java")

ENTRY = re.compile(r'<imgdir name="(\d+)">(.*?)</imgdir>', re.S)
FIELD = re.compile(r'<(?:int|short|long|string|float) name="(\w+)" value="([^"]*)"')


def read(path, limit=None):
    with open(path, encoding="utf-8", errors="ignore") as f:
        return f.read(limit) if limit else f.read()


def string_entries(name):
    """id -> {field: value} for one String.wz file."""
    out = {}
    for m in ENTRY.finditer(read(os.path.join(WZ, "String.wz", name + ".img.xml"))):
        fields = dict((k, html.unescape(v)) for k, v in FIELD.findall(m.group(2)))
        out[int(m.group(1))] = fields
    return out


def info_block(path):
    """The fields of the first <imgdir name="info"> block of a data file."""
    text = read(path, 40000)
    start = text.find('<imgdir name="info">')
    if start < 0:
        return {}
    # Only the block's own fields count: nested blocks (a boss's skill list, an item's level-up table)
    # have fields with the same names, such as "level".
    fields, depth = {}, 0
    for line in text[start:].splitlines():
        s = line.strip()
        if s.startswith("<imgdir"):
            depth += 1
        elif s.startswith("</imgdir"):
            depth -= 1
            if depth == 0:
                break
        elif depth == 1:
            m = FIELD.match(s)
            if m:
                fields.setdefault(m.group(1), m.group(2))
    return fields


def file_index(folder):
    """id -> path for every NNNN.img.xml under a wz folder."""
    out = {}
    for dp, _, files in os.walk(os.path.join(WZ, folder)):
        for f in files:
            m = re.match(r"0*(\d+)\.img\.xml$", f)
            if m:
                out[int(m.group(1))] = os.path.join(dp, f)
    return out


def write(name, header, rows):
    path = os.path.join(HERE, name)
    with open(path, "w", encoding="utf-8", newline="\n") as f:
        f.write("\t".join(header) + "\n")
        for r in rows:
            f.write("\t".join(str(c).replace("\t", " ").replace("\n", " ") for c in r) + "\n")
    print(f"{name}: {len(rows)} rows")


def jobs():
    found = re.findall(r"\b([A-Z][A-Z0-9_]+)\((\d+)\)", read(JOB_JAVA))
    by_id = {int(i): n for n, i in found}
    write("Jobs.tsv", ["id", "name"], sorted(by_id.items()))
    return by_id


def skills(job_names):
    rows = []
    for sid, f in sorted(string_entries("Skill").items()):
        if "name" not in f:
            continue
        job = sid // 10000
        levels = len([k for k in f if re.fullmatch(r"h\d+", k)])
        rows.append((sid, job, job_names.get(job, ""), f["name"], levels or ""))
    write("Skills.tsv", ["id", "job_id", "job", "name", "max_level"], rows)


def maps():
    rows = [(mid, f.get("streetName", ""), f.get("mapName", ""))
            for mid, f in sorted(string_entries("Map").items())]
    write("Maps.tsv", ["id", "area", "name"], rows)


def mobs():
    names = string_entries("Mob")
    rows = []
    for mid, path in sorted(file_index("Mob.wz").items()):
        i = info_block(path)
        rows.append((mid, names.get(mid, {}).get("name", ""), i.get("level", ""), i.get("maxHP", ""),
                     i.get("exp", ""), "boss" if i.get("boss") == "1" else ""))
    write("Mobs.tsv", ["id", "name", "level", "hp", "exp", "boss"], rows)


def npcs():
    rows = [(nid, f.get("name", ""), f.get("func", "")) for nid, f in sorted(string_entries("Npc").items())]
    write("Npcs.tsv", ["id", "name", "role"], rows)


JOB_BITS = [(1, "warrior"), (2, "magician"), (4, "bowman"), (8, "thief"), (16, "pirate")]


def equips():
    names = string_entries("Eqp")
    rows = []
    for iid, path in sorted(file_index("Character.wz").items()):
        if iid < 1000000:      # faces, hair, body parts
            continue
        i = info_block(path)
        bits = int(i.get("reqJob", "0") or 0)
        job = "all" if bits <= 0 else "/".join(n for b, n in JOB_BITS if bits & b)
        stats = " ".join(f"{k[3:]}+{v}" for k, v in i.items() if k.startswith("inc") and v not in ("0", ""))
        rows.append((iid, names.get(iid, {}).get("name", ""), os.path.basename(os.path.dirname(path)),
                     i.get("reqLevel", ""), job, i.get("tuc", ""), "cash" if i.get("cash") == "1" else "", stats,
                     i.get("reqSTR", "0"), i.get("reqDEX", "0"), i.get("reqINT", "0"), i.get("reqLUK", "0"),
                     i.get("reqPOP", "0")))
    write("Equips.tsv", ["id", "name", "type", "req_level", "job", "slots", "cash", "stats",
                         "req_str", "req_dex", "req_int", "req_luk", "req_fame"], rows)


def items():
    rows = []
    for name, kind in [("Consume", "use"), ("Ins", "setup"), ("Etc", "etc"), ("Cash", "cash"), ("Pet", "pet")]:
        for iid, f in sorted(string_entries(name).items()):
            if "name" in f:
                rows.append((iid, f["name"], kind, re.sub(r"\\[nr]|#c|#", " ", f.get("desc", ""))[:120]))
    rows.sort()
    write("Items.tsv", ["id", "name", "kind", "description"], rows)


MYSQL = os.path.join(ROOT, "Tools", "mysql", "bin", "mysql.exe")
MYINI = os.path.join(ROOT, "Settings", "mysql.ini")
SRC = os.path.join(ROOT, "Server", "src", "main", "java")


def query(sql):
    """Rows from the game database (the database must be running)."""
    out = subprocess.run([MYSQL, "--defaults-file=" + MYINI, "-N", "-B", "cosmic", "-e", sql],
                         capture_output=True, text=True, encoding="utf-8", errors="ignore")
    if out.returncode != 0:
        raise RuntimeError(out.stderr.strip())
    return [line.split("\t") for line in out.stdout.splitlines()]


def all_item_names():
    names = {}
    for f in ("Eqp", "Consume", "Ins", "Etc", "Cash", "Pet"):
        for iid, fields in string_entries(f).items():
            if "name" in fields:
                names[iid] = fields["name"]
    return names


def pct(chance):
    """Drop chances are stored out of 1,000,000."""
    return f"{int(chance) / 10000:.4f}".rstrip("0").rstrip(".")


def drops(item_names):
    mob_names = {k: v.get("name", "") for k, v in string_entries("Mob").items()}
    rows = []
    for mob, item, lo, hi, quest, chance in query(
            "SELECT dropperid,itemid,minimum_quantity,maximum_quantity,questid,chance FROM drop_data "
            "ORDER BY dropperid,chance DESC"):
        name = "(meso)" if item == "0" else item_names.get(int(item), "")
        rows.append((mob, mob_names.get(int(mob), ""), item, name, lo, hi, pct(chance), quest if quest != "0" else ""))
    for item, lo, hi, quest, chance, comment in query(
            "SELECT itemid,minimum_quantity,maximum_quantity,questid,chance,comments FROM drop_data_global "
            "ORDER BY chance DESC"):
        rows.append(("all", "(every monster)", item, item_names.get(int(item), comment), lo, hi, pct(chance),
                     quest if quest != "0" else ""))
    write("Drops.tsv", ["mob_id", "mob", "item_id", "item", "min", "max", "chance_percent", "quest_id"], rows)


def shops(item_names):
    npc_names = {k: v.get("name", "") for k, v in string_entries("Npc").items()}
    rows = []
    for shop, npc, item, price, pitch in query(
            "SELECT s.shopid,s.npcid,i.itemid,i.price,i.pitch FROM shops s JOIN shopitems i ON i.shopid=s.shopid "
            "ORDER BY s.npcid,i.position"):
        rows.append((shop, npc, npc_names.get(int(npc), ""), item, item_names.get(int(item), ""), price,
                     pitch if pitch != "0" else ""))
    write("Shops.tsv", ["shop_id", "npc_id", "npc", "item_id", "item", "price_meso", "price_perfect_pitch"], rows)


def scrolls(item_names):
    root = ET.parse(os.path.join(WZ, "Item.wz", "Consume", "0204.img.xml")).getroot()
    rows = []
    for item in root:
        iid = int(item.get("name"))
        info = item.find("imgdir[@name='info']")
        f = {c.get("name"): c.get("value") for c in info if c.get("value") is not None} if info is not None else {}
        stats = " ".join(f"{k[3:]}+{v}" for k, v in f.items() if k.startswith("inc"))
        other = " ".join(f"{k}={v}" for k, v in f.items()
                         if not k.startswith("inc") and k not in ("success", "cursed", "price", "slotMax", "icon", "iconRaw"))
        rows.append((iid, item_names.get(iid, ""), f.get("success", ""), f.get("cursed", ""), stats, other))
    write("Scrolls.tsv", ["id", "name", "success_percent", "destroy_percent", "stats", "other"], rows)


SKILL_COLS = ["mpCon", "hpCon", "damage", "pad", "mad", "attackCount", "mobCount", "time", "cooltime", "x", "y", "z",
              "prop", "mastery", "speed", "jump", "range"]
SKILL_SKIP = {"hs", "action", "ball", "hit", "lt", "rb"}


def skill_details(job_names):
    names = {k: v.get("name", "") for k, v in string_entries("Skill").items()}
    rows = []
    for path in sorted(glob.glob(os.path.join(WZ, "Skill.wz", "*.img.xml"))):
        skill_root = ET.parse(path).getroot().find("imgdir[@name='skill']")
        if skill_root is None:
            continue
        for skill in skill_root:
            sid = int(skill.get("name"))
            levels = skill.find("imgdir[@name='level']")
            if levels is None:
                continue
            for lv in sorted(levels, key=lambda e: int(e.get("name"))):
                f = {c.get("name"): c.get("value") for c in lv if c.get("value") is not None}
                other = " ".join(f"{k}={v}" for k, v in f.items() if k not in SKILL_COLS and k not in SKILL_SKIP)
                rows.append([sid, names.get(sid, ""), job_names.get(sid // 10000, ""), lv.get("name")]
                            + [f.get(c, "") for c in SKILL_COLS] + [other])
    rows.sort(key=lambda r: (r[0], int(r[3])))
    write("SkillDetails.tsv", ["skill_id", "skill", "job", "level"] + SKILL_COLS + ["other"], rows)


def quests():
    info = ET.parse(os.path.join(WZ, "Quest.wz", "QuestInfo.img.xml")).getroot()
    check = {e.get("name"): e for e in ET.parse(os.path.join(WZ, "Quest.wz", "Check.img.xml")).getroot()}
    rows = []
    for q in info:
        qid = q.get("name")
        f = {c.get("name"): c.get("value") or "" for c in q}
        start = {}
        mobs_needed, items_needed = [], []
        c = check.get(qid)
        if c is not None:
            s = c.find("imgdir[@name='0']")
            if s is not None:
                start = {x.get("name"): x.get("value") for x in s if x.get("value") is not None}
            e = c.find("imgdir[@name='1']")
            if e is not None:
                for kind, out in (("mob", mobs_needed), ("item", items_needed)):
                    block = e.find(f"imgdir[@name='{kind}']")
                    if block is not None:
                        for entry in block:
                            v = {x.get("name"): x.get("value") for x in entry}
                            out.append(f"{v.get('id', '')}x{v.get('count', '')}")
        rows.append((int(qid), f.get("name", ""), f.get("area", ""), start.get("npc", ""), start.get("lvmin", ""),
                     start.get("lvmax", ""), " ".join(mobs_needed), " ".join(items_needed)))
    rows.sort()
    write("Quests.tsv", ["id", "name", "area", "start_npc", "min_level", "max_level", "kill_mobs", "collect_items"], rows)


def commands():
    text = read(os.path.join(SRC, "client", "command", "CommandsExecutor.java"))
    files = {os.path.basename(p)[:-5]: p
             for p in glob.glob(os.path.join(SRC, "client", "command", "commands", "**", "*.java"), recursive=True)}
    rows = []
    level = 0
    for line in text.splitlines():
        m = re.search(r"private void registerLv(\d)Commands", line)
        if m:
            level = int(m.group(1))
        m = re.search(r'addCommand\((new String\[\]\{[^}]*\}|"[^"]+")\s*,\s*(?:(\d)\s*,\s*)?(\w+)\.class', line)
        if not m:
            continue
        names = re.findall(r'"([^"]+)"', m.group(1))
        lv = int(m.group(2)) if m.group(2) else level
        desc = ""
        if m.group(3) in files:
            d = re.search(r'setDescription\("([^"]*)"', read(files[m.group(3)]))
            desc = d.group(1) if d else ""
        prefix = "@" if lv == 0 else "!"
        rows.append((lv, " ".join(prefix + n for n in names), desc))
    rows.sort()
    write("Commands.tsv", ["gm_level", "command", "description"], rows)


LIFE = re.compile(r'<imgdir name="\d+">\s*<string name="type" value="m"/>\s*<string name="id" value="(\d+)"/>(.*?)</imgdir>',
                  re.S)


def mob_spawns():
    """Which monsters spawn on which map, from the map files."""
    mob_names = {k: v.get("name", "") for k, v in string_entries("Mob").items()}
    map_names = string_entries("Map")
    rows = []
    for path in glob.glob(os.path.join(WZ, "Map.wz", "Map", "Map*", "*.img.xml")):
        m = re.match(r"0*(\d+)\.img\.xml$", os.path.basename(path))
        if not m:
            continue
        map_id = int(m.group(1))
        text = read(path)
        start = text.find('<imgdir name="life">')
        if start < 0:
            continue
        counts, respawn = {}, {}
        for mob, rest in LIFE.findall(text[start:]):
            mob = int(mob)
            counts[mob] = counts.get(mob, 0) + 1
            t = re.search(r'<int name="mobTime" value="(-?\d+)"', rest)
            respawn[mob] = max(respawn.get(mob, 0), int(t.group(1)) if t else 0)
        place = map_names.get(map_id, {})
        for mob, n in counts.items():
            rows.append((mob, mob_names.get(mob, ""), map_id, place.get("streetName", ""), place.get("mapName", ""), n,
                         respawn[mob] if respawn[mob] > 0 else ""))
    rows.sort()
    write("MobSpawns.tsv", ["mob_id", "mob", "map_id", "area", "map", "count", "respawn_seconds"], rows)


if __name__ == "__main__":
    job_names = jobs()
    skills(job_names)
    maps()
    mobs()
    npcs()
    equips()
    items()
    scrolls(all_item_names())
    skill_details(job_names)
    quests()
    commands()
    mob_spawns()
    # These two read the database, so it must be running.
    drops(all_item_names())
    shops(all_item_names())
