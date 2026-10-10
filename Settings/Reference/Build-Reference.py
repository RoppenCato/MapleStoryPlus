"""Rebuilds the ID reference lists in this folder from the server's game data (Server/wz).

Run again after editing the game data:  python Settings/Reference/Build-Reference.py
"""
import html
import os
import re

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
    text = read(path, 12000)
    m = re.search(r'<imgdir name="info">(.*?)</imgdir>', text, re.S)
    return dict(FIELD.findall(m.group(1))) if m else {}


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
                     i.get("reqLevel", ""), job, i.get("tuc", ""), "cash" if i.get("cash") == "1" else "", stats))
    write("Equips.tsv", ["id", "name", "type", "req_level", "job", "slots", "cash", "stats"], rows)


def items():
    rows = []
    for name, kind in [("Consume", "use"), ("Ins", "setup"), ("Etc", "etc"), ("Cash", "cash"), ("Pet", "pet")]:
        for iid, f in sorted(string_entries(name).items()):
            if "name" in f:
                rows.append((iid, f["name"], kind, re.sub(r"\\[nr]|#c|#", " ", f.get("desc", ""))[:120]))
    rows.sort()
    write("Items.tsv", ["id", "name", "kind", "description"], rows)


if __name__ == "__main__":
    job_names = jobs()
    skills(job_names)
    maps()
    mobs()
    npcs()
    equips()
    items()
