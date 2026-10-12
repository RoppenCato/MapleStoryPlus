"""Sets up a test character: level, job, stats, skills, gear and supplies.

Examples (run from the project folder, with the database running and the character logged out):

    python Settings/Scripts/Make-Character.py trialguy fp 50
    python Settings/Scripts/Make-Character.py DevBandit bandit 60 --create
    python Settings/Scripts/Make-Character.py DevBandit bandit 60 --dry-run
    python Settings/Scripts/Make-Character.py --loadouts        (rewrites Settings/Reference/Loadouts.tsv)

Gear is picked from Settings/Reference/Equips.tsv: the highest-level normal-progression item per slot.
"Normal progression" means made for the class, sold in a shop or dropped by at least two ordinary
monsters, and not a Maple, event or boss item. Corrections go in Loadout-Overrides.tsv.
Skills follow Skill-Builds.tsv, in order, limited by the skill points the level gives.
"""
import argparse
import collections
import datetime
import io
import os
import re
import subprocess
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(os.path.dirname(HERE))
REF = os.path.join(ROOT, "Settings", "Reference")
WZ = os.path.join(ROOT, "Server", "wz")
MYSQL = os.path.join(ROOT, "Tools", "mysql", "bin", "mysql.exe")
MYSQLDUMP = os.path.join(ROOT, "Tools", "mysql", "bin", "mysqldump.exe")
MYINI = os.path.join(ROOT, "Settings", "mysql.ini")

# line: (class, first/second/third job, weapon id prefixes, uses a shield, main stat, ammo kind)
LINES = {
    "hero":       ("warrior",  (100, 110, 111), ("140",),       False, "str", None),
    "paladin":    ("warrior",  (100, 120, 121), ("130",),       True,  "str", None),
    "darkknight": ("warrior",  (100, 130, 131), ("143",),       False, "str", None),
    "fp":         ("magician", (200, 210, 211), ("137", "138"), True,  "int", None),
    "il":         ("magician", (200, 220, 221), ("137", "138"), True,  "int", None),
    "cleric":     ("magician", (200, 230, 231), ("137", "138"), True,  "int", None),
    "hunter":     ("bowman",   (300, 310, 311), ("145",),       False, "dex", "bow"),
    "crossbow":   ("bowman",   (300, 320, 321), ("146",),       False, "dex", "crossbow"),
    "assassin":   ("thief",    (400, 410, 411), ("147",),       False, "luk", "star"),
    "bandit":     ("thief",    (400, 420, 421), ("133",),       True,  "luk", None),
    "brawler":    ("pirate",   (500, 510, 511), ("148",),       False, "str", None),
    "gunslinger": ("pirate",   (500, 520, 521), ("149",),       False, "dex", "bullet"),
}
ALIASES = {
    "fighter": "hero", "crusader": "hero", "sword": "hero", "page": "paladin", "whiteknight": "paladin",
    "spearman": "darkknight", "dragonknight": "darkknight", "dk": "darkknight", "spear": "darkknight",
    "firemage": "fp", "fire": "fp", "poison": "fp", "mage": "fp", "wizard": "fp", "icemage": "il", "ice": "il",
    "lightning": "il", "priest": "cleric", "bishop": "cleric", "ranger": "hunter", "bowmaster": "hunter",
    "bow": "hunter", "bowman": "hunter", "sniper": "crossbow", "crossbowman": "crossbow", "marksman": "crossbow",
    "sin": "assassin", "hermit": "assassin", "nightlord": "assassin", "claw": "assassin", "thief": "assassin",
    "chiefbandit": "bandit", "shadower": "bandit", "dagger": "bandit", "marauder": "brawler", "buccaneer": "brawler",
    "knuckle": "brawler", "outlaw": "gunslinger", "corsair": "gunslinger", "gun": "gunslinger", "pirate": "brawler",
    "warrior": "hero",
}
LEVELS = (10, 20, 30, 40, 50, 60, 70, 80, 90, 100)

# slot: (equip position, type folder in Equips.tsv, id prefix or None)
SLOTS = {
    "hat": (-1, "Cap", None), "earrings": (-4, "Accessory", "103"), "top": (-5, "Coat", None),
    "overall": (-5, "Longcoat", None), "bottom": (-6, "Pants", None), "shoes": (-7, "Shoes", None),
    "gloves": (-8, "Glove", None), "cape": (-9, "Cape", None), "shield": (-10, "Shield", None),
    "weapon": (-11, "Weapon", None),
}
GENERIC_SLOTS = ("earrings", "cape")      # not tied to a class
STAT_COL = {"STR": "str", "DEX": "dex", "INT": "int", "LUK": "luk", "MHP": "hp", "MMP": "mp", "PAD": "watk",
            "MAD": "matk", "PDD": "wdef", "MDD": "mdef", "ACC": "acc", "EVA": "avoid", "Speed": "speed",
            "Jump": "jump"}
SPECIAL_NAME = re.compile(r"Maple|MISSING|Balrog|Beginner|Anniv|Flag|Astaroth|King Pepe|Seraphim|Raven|Timeless|"
                          r"Reverse|Elemental|Nebula|Bain|Crimson|Flower Tube|Transformation|Maku|Akha|Kuma|Umaru|Xaru|"
                          r"Toenail|Baseball|Bathrobe|Sauna|Bosshunter|Korean Fan|Plastic Bottle|Japanese Map|Legendary|Amos|Cecelia|"
                          r"Stirgeman|Sirius", re.I)

# (up to level, HP potion, MP potion)
POTIONS = [(19, 2000000, 2000003), (29, 2000001, 2000003), (49, 2000002, 2000006), (79, 2022003, 2022000),
           (999, 2001001, 2001002)]
ARROWS = {"bow": [(29, 2060000), (69, 2060001), (999, 2060003)],
          "crossbow": [(29, 2061000), (69, 2061001), (999, 2061003)]}
STARS = (2070000, 2070001, 2070002, 2070003, 2070004, 2070005, 2070006, 2070007)
BULLETS = (2330000, 2330001, 2330002, 2330003, 2330004, 2330005)
MAGIC_ROCK, SUMMONING_ROCK = 4006000, 4006001


def tsv(path):
    with io.open(path, encoding="utf-8") as f:
        rows = [line.rstrip("\n").split("\t") for line in f if line.strip()]
    return [dict(zip(rows[0], r + [""] * (len(rows[0]) - len(r)))) for r in rows[1:]]


class Data:
    def __init__(self):
        mobs = {m["id"]: m for m in tsv(os.path.join(REF, "Mobs.tsv"))}
        self.breadth = collections.Counter()
        for d in tsv(os.path.join(REF, "Drops.tsv")):
            if d["mob_id"] != "all" and mobs.get(d["mob_id"], {}).get("boss") != "boss":
                self.breadth[d["item_id"]] += 1
        self.in_shop = {s["item_id"] for s in tsv(os.path.join(REF, "Shops.tsv"))}
        self.equips = [e for e in tsv(os.path.join(REF, "Equips.tsv")) if e["cash"] != "cash" and e["name"]]
        self.equip_by_id = {e["id"]: e for e in self.equips}
        self.item_names = {i["id"]: i["name"] for i in tsv(os.path.join(REF, "Items.tsv"))}
        self.skills = collections.defaultdict(dict)       # job id -> name -> (skill id, max level)
        for s in tsv(os.path.join(REF, "Skills.tsv")):
            self.skills[int(s["job_id"])][s["name"]] = (int(s["id"]), int(s["max_level"] or 0))
        self.builds = collections.defaultdict(list)       # (line, job id) -> [(skill name, level)]
        for b in tsv(os.path.join(HERE, "Skill-Builds.tsv")):
            self.builds[(b["line"], int(b["job_id"]))].append((b["skill"], int(b["level"])))
        self.overrides = {}
        path = os.path.join(HERE, "Loadout-Overrides.tsv")
        if os.path.exists(path):
            for o in tsv(path):
                self.overrides[(o["line"], int(o["level"]), o["gender"], o["slot"])] = o["item_id"]
        self._item_info = {}

    def item_info(self, item_id):
        """slotMax and reqLevel of a use or etc item, read from the game data."""
        if item_id not in self._item_info:
            folder = {2: "Consume", 4: "Etc"}[item_id // 1000000]
            path = os.path.join(WZ, "Item.wz", folder, "%04d.img.xml" % (item_id // 10000))
            info = {}
            if os.path.exists(path):
                with io.open(path, encoding="utf-8", errors="ignore") as f:
                    text = f.read()
                m = re.search(r'<imgdir name="%08d">(.*?)<imgdir name="\d{8}">' % item_id, text + '<imgdir name="00000000">', re.S)
                if m:
                    info = dict(re.findall(r'<(?:int|short) name="(slotMax|reqLevel)" value="(\d+)"', m.group(1)))
            self._item_info[item_id] = (int(info.get("slotMax", 100)), int(info.get("reqLevel", 0)))
        return self._item_info[item_id]


def gender_ok(item_id, gender):
    if item_id >= 1300000:
        return True
    g = (item_id // 1000) % 10
    return g >= 2 or g == gender


def pick(data, cls, level, gender, slot, prefixes=None):
    """Best normal-progression item for a slot, or None. Returns (equip row, how sure we are)."""
    _, folder, slot_prefix = SLOTS[slot]
    pool = []
    for e in data.equips:
        if e["type"] != folder or not e["req_level"]:
            continue
        iid = int(e["id"])
        if slot_prefix and not e["id"].startswith(slot_prefix):
            continue
        if prefixes and not e["id"].startswith(prefixes):
            continue
        if int(e["req_level"]) > level or not gender_ok(iid, gender) or SPECIAL_NAME.search(e["name"]):
            continue
        pool.append(e)
    jobs_of = lambda e: e["job"].split("/")
    everyone = [e for e in pool if e["job"] == "all"]
    own = [e for e in pool if cls in jobs_of(e)]
    standard = lambda e: e["id"] in data.in_shop or data.breadth[e["id"]] >= 2
    if slot in GENERIC_SLOTS:
        tiers = [("standard", own + everyone, standard), ("one drop source", own + everyone, lambda e: data.breadth[e["id"]] >= 1)]
    else:
        tiers = [("standard", own, standard), ("standard, any class", everyone, standard),
                 ("one drop source", own, lambda e: data.breadth[e["id"]] >= 1), ("unverified", own, lambda e: True)]
    for label, candidates, test in tiers:
        found = [e for e in candidates if test(e)]
        if found:
            best = max(found, key=lambda e: (int(e["req_level"]), e["job"] == cls, e["id"] in data.in_shop,
                                             data.breadth[e["id"]], -int(e["id"])))
            return best, label
    return None, ""


def loadout(data, line, level, gender):
    """slot -> (equip row, confidence) for a line at a level."""
    cls, _, weapon_prefixes, shield, _, _ = LINES[line]
    g = "m" if gender == 0 else "f"
    chosen = {}
    for slot in SLOTS:
        if slot == "shield" and not shield:
            continue
        key = (line, level, g, slot)
        any_key = (line, level, "any", slot)
        override = data.overrides.get(key) or data.overrides.get(any_key)
        if override:
            if override != "none" and override in data.equip_by_id:
                chosen[slot] = (data.equip_by_id[override], "override")
            continue
        item, label = pick(data, cls, level, gender, slot, weapon_prefixes if slot == "weapon" else None)
        if item:
            chosen[slot] = (item, label)
    # An overall replaces top and bottom when it is at least as good as both.
    lvl = lambda s: int(chosen[s][0]["req_level"]) if s in chosen else -1
    separates = "top" in chosen and "bottom" in chosen
    overall_is_solid = "overall" in chosen and chosen["overall"][1] == "standard"
    if "overall" in chosen and (not separates or (overall_is_solid and lvl("overall") >= max(lvl("top"), lvl("bottom")))):
        chosen.pop("top", None)
        chosen.pop("bottom", None)
    else:
        chosen.pop("overall", None)
    return chosen


def job_at(line, level):
    cls, (j1, j2, j3), *_ = LINES[line]
    first = 8 if cls == "magician" else 10
    if level < first:
        return 0
    if level < 30:
        return j1
    if level < 70:
        return j2
    return j3 if level < 120 else j3 + 1


def skill_points(line, level):
    """Skill points earned in each job, as {job id: points}."""
    cls, (j1, j2, j3), *_ = LINES[line]
    first = 8 if cls == "magician" else 10
    out = {}
    if level >= first:
        out[j1] = 1 + 3 * (min(level, 30) - first)
    if level >= 30:
        out[j2] = 1 + 3 * (min(level, 70) - 30)
    if level >= 70:
        out[j3] = 1 + 3 * (min(level, 120) - 70)
    if level >= 120:
        out[j3 + 1] = 3 + 3 * (level - 120)             # 4th job
    return out


def build_skills(data, line, level, mode="build"):
    """[(skill id, name, level)]. mode "build" follows Skill-Builds.tsv within the skill points the level
    gives; "max" gives every skill of the jobs reached at its max level, for testing; "none" gives nothing."""
    result = []
    if mode == "none":
        return result
    if mode == "max":
        for job in skill_points(line, level):
            for name, (sid, max_level) in sorted(data.skills[job].items(), key=lambda kv: kv[1][0]):
                if max_level > 0:
                    result.append((sid, name, max_level))
        return result
    for job, points in skill_points(line, level).items():
        for name, want in data.builds.get((line, job), []):
            if name not in data.skills[job]:
                raise SystemExit(f"Skill-Builds.tsv: no skill named '{name}' in job {job}")
            sid, max_level = data.skills[job][name]
            give = min(want, max_level or want, points)
            if give > 0:
                result.append((sid, name, give))
                points -= give
    return result


def stats_for(line, level, gear):
    _, _, _, _, main, _ = LINES[line]
    total = 20 + 5 * level
    stats = {"str": 4, "dex": 4, "int": 4, "luk": 4}
    for item, _ in gear.values():
        for s in stats:
            if s != main:
                stats[s] = max(stats[s], int(item.get("req_" + s) or 0))
    stats[main] = total - sum(v for k, v in stats.items() if k != main)
    fame = max([int(item.get("req_fame") or 0) for item, _ in gear.values()] or [0])
    return stats, fame


def hp_mp(line, level):
    """Rough HP and MP for the class at this level. Estimates, not the game's exact growth."""
    cls = LINES[line][0]
    if cls == "warrior":
        return 60 * level, 8 * level + 50
    if cls == "magician":
        return 12 * level + 100, 55 * level
    if line == "brawler":
        return 40 * level, 14 * level + 50
    return 22 * level + 100, 15 * level + 100


AMMO_BY_WEAPON = {"145": "bow", "146": "crossbow", "147": "star", "149": "bullet"}


def supplies(data, line, level, gear):
    """[(item id, quantity, inventory type)]"""
    cls = LINES[line][0]
    weapon = gear["weapon"][0]["id"] if "weapon" in gear else ""
    ammo = AMMO_BY_WEAPON.get(weapon[:3])     # follows the weapon actually equipped
    hp_pot, mp_pot = next((h, m) for cap, h, m in POTIONS if level <= cap)
    mage = cls == "magician"
    out = [(hp_pot, 100 if mage else 300, 2), (mp_pot, 600 if mage else 300, 2)]
    if ammo in ARROWS:
        out.append((next(i for cap, i in ARROWS[ammo] if level <= cap), 3 * data.item_info(2060000)[0], 2))
    elif ammo in ("star", "bullet"):
        options = [i for i in (STARS if ammo == "star" else BULLETS) if data.item_info(i)[1] <= level]
        best = max(options, key=lambda i: (data.item_info(i)[1], i)) if options else (STARS if ammo == "star" else BULLETS)[0]
        out.append((best, 4 * data.item_info(best)[0], 2))
    if mage and level >= 70:
        out.append((MAGIC_ROCK, 100, 4))
    if line == "assassin" and level >= 70:
        out.append((SUMMONING_ROCK, 200, 4))
    if cls == "bowman" and level >= 70:
        out.append((SUMMONING_ROCK, 100, 4))
    return out


# ---------------------------------------------------------------- database

def sql_run(sql, fetch=False):
    args = [MYSQL, "--defaults-file=" + MYINI, "cosmic"] + (["-N", "-B"] if fetch else [])
    out = subprocess.run(args, input=sql, capture_output=True, text=True, encoding="utf-8", errors="ignore")
    if out.returncode != 0:
        raise SystemExit("Database error: " + out.stderr.strip())
    return [line.split("\t") for line in out.stdout.splitlines()] if fetch else None


def find_character(name):
    rows = sql_run("SELECT c.id, c.gender, a.loggedin, c.accountid FROM characters c JOIN accounts a "
                   f"ON a.id = c.accountid WHERE c.name = '{name}';", fetch=True)
    return [int(x) for x in rows[0]] if rows else None


def create_character(name, template, gender):
    if not re.fullmatch(r"[A-Za-z0-9]{3,12}", name):
        raise SystemExit("Character names are 3-12 letters or digits.")
    source = find_character(template)
    if not source:
        raise SystemExit(f"Template character '{template}' not found.")
    cols = [r[0] for r in sql_run("SELECT column_name FROM information_schema.columns WHERE table_schema='cosmic' "
                                  "AND table_name='characters' ORDER BY ordinal_position;", fetch=True)]
    cols = [c for c in cols if c.lower() != "id"]
    select = [f"'{name}'" if c == "name" else f"`{c}`" for c in cols]
    look = ""
    if gender is not None and gender != source[1]:
        hair, face = (30000, 20000) if gender == 0 else (31000, 21000)
        look = f", gender = {gender}, hair = {hair}, face = {face}"
    sql_run(f"INSERT INTO characters ({', '.join('`' + c + '`' for c in cols)}) "
            f"SELECT {', '.join(select)} FROM characters WHERE id = {source[0]};\n"
            f"SET @new := LAST_INSERT_ID();\n"
            f"UPDATE characters SET map = 100000000, spawnpoint = 0, meso = 0, fame = 0, exp = 0{look} WHERE id = @new;\n"
            f"INSERT INTO keymap (characterid, `key`, `type`, `action`) "
            f"SELECT @new, `key`, `type`, `action` FROM keymap WHERE characterid = {source[0]};")


NIMBLE_FEET = 1002      # the sprint; every test character gets it on Shift
KEY_SHIFT = 42


def apply(data, name, line, level, meso, dry_run, check=False, skill_mode="build", spare_sp=0):
    found = find_character(name)
    if not found:
        raise SystemExit(f"Character '{name}' not found. Create it in the game, or add --create.")
    cid, gender, logged_in, _ = found
    gear = loadout(data, line, level, gender)
    skills = build_skills(data, line, level, skill_mode)
    stats, fame = stats_for(line, level, gear)
    hp, mp = hp_mp(line, level)
    items = supplies(data, line, level, gear)
    job = job_at(line, level)

    print(f"{name}: level {level} {line} (job {job}), {'male' if gender == 0 else 'female'}")
    print(f"  Stats  STR {stats['str']}  DEX {stats['dex']}  INT {stats['int']}  LUK {stats['luk']}  HP {hp}  MP {mp}")
    for slot in SLOTS:
        if slot in gear:
            item, label = gear[slot]
            note = "" if label == "standard" else f"  [{label}]"
            print(f"  {slot:9}{item['name']} (level {item['req_level']}, id {item['id']}){note}")
    print("  Skills " + (", ".join(f"{n} {lv}" for _, n, lv in skills) or "none")
          + (f"  (+{spare_sp} unspent skill points)" if spare_sp else ""))
    print("  Items  " + ", ".join(f"{data.item_names.get(str(i), i)} x{q}" for i, q, _ in items))
    if dry_run:
        print("Dry run: nothing changed.")
        return
    if logged_in != 0 and not check:
        raise SystemExit("The character's account is logged in. Log out (close the game) and run again.")
    if check:
        print("Check mode: running the changes against the database, then undoing them.")

    backup = os.path.join(ROOT, "Backups")
    os.makedirs(backup, exist_ok=True)
    stamp = datetime.datetime.now().strftime("%Y-%m-%d_%H%M%S")
    dump = None if check else subprocess.run([MYSQLDUMP, "--defaults-file=" + MYINI, "--single-transaction", "--routines", "--databases",
                           "cosmic", "--result-file=" + os.path.join(backup, f"cosmic_{stamp}_before-{name}.sql")],
                          capture_output=True, text=True)
    if dump is not None and dump.returncode != 0:
        raise SystemExit("Backup failed, nothing changed: " + dump.stderr.strip())

    used = {int(t): int(n) for t, n in sql_run(
        f"SELECT inventorytype, COALESCE(MAX(position), 0) FROM inventoryitems WHERE characterid = {cid} "
        "AND inventorytype > 0 GROUP BY inventorytype;", fetch=True)}
    give_ids = ",".join(str(i) for i, _, _ in items)
    worn = int(sql_run(f"SELECT COUNT(*) FROM inventoryitems WHERE characterid = {cid} AND inventorytype = -1 "
                       "AND position > -100;", fetch=True)[0][0])
    q = ["START TRANSACTION;"]
    if used.get(1, 0) + worn <= 24:
        # old equipped gear goes to the equip inventory
        q += [f"SET @n := {used.get(1, 0)};",
              f"UPDATE inventoryitems SET inventorytype = 1, position = (@n := @n + 1) WHERE characterid = {cid} "
              "AND inventorytype = -1 AND position > -100 ORDER BY position DESC;"]
    else:
        print("  The equip inventory is full, so the old equipped gear is removed instead of kept.")
        q += [f"DELETE e FROM inventoryequipment e JOIN inventoryitems i USING (inventoryitemid) "
              f"WHERE i.characterid = {cid} AND i.inventorytype = -1 AND i.position > -100;",
              f"DELETE FROM inventoryitems WHERE characterid = {cid} AND inventorytype = -1 AND position > -100;"]
    q += [
         f"DELETE FROM inventoryitems WHERE characterid = {cid} AND inventorytype IN (2, 4) AND itemid IN ({give_ids});",
         f"DELETE FROM skills WHERE characterid = {cid} AND skillid BETWEEN 1000000 AND 5999999;"]
    insert = ("INSERT INTO inventoryitems (type, characterid, itemid, inventorytype, position, quantity, owner, petid, "
              "flag, expiration, giftFrom) VALUES (1, {cid}, {item}, {inv}, {pos}, {qty}, '', -1, 0, -1, '');")
    for slot, (item, _) in gear.items():
        q.append(insert.format(cid=cid, item=item["id"], inv=-1, pos=SLOTS[slot][0], qty=1))
        cols, vals = ["inventoryitemid", "upgradeslots"], ["LAST_INSERT_ID()", item["slots"] or "0"]
        for part in item["stats"].split():
            key, value = part.split("+")
            if key in STAT_COL:
                cols.append("`" + STAT_COL[key] + "`")
                vals.append(value)
        q.append(f"INSERT INTO inventoryequipment ({', '.join(cols)}) VALUES ({', '.join(vals)});")
    next_pos = {2: 0, 4: 0}
    positions = {int(t): {int(p) for p in ps.split(",")} for t, ps in sql_run(
        f"SELECT inventorytype, GROUP_CONCAT(position) FROM inventoryitems WHERE characterid = {cid} "
        f"AND inventorytype IN (2, 4) AND itemid NOT IN ({give_ids}) GROUP BY inventorytype;", fetch=True)}
    for item_id, quantity, inv in items:
        stack = data.item_info(item_id)[0]
        while quantity > 0:
            next_pos[inv] += 1
            while next_pos[inv] in positions.get(inv, ()):
                next_pos[inv] += 1
            q.append(insert.format(cid=cid, item=item_id, inv=inv, pos=next_pos[inv], qty=min(stack, quantity)))
            quantity -= stack
    for sid, _, lv in skills:
        # A 4th job skill can only be raised as far as its master level, so that is set along with it
        master = lv if sid // 10000 % 10 == 2 else 0
        q.append(f"INSERT INTO skills (skillid, characterid, skilllevel, masterlevel, expiration) "
                 f"VALUES ({sid}, {cid}, {lv}, {master}, -1);")
    # Sprint for everyone, and no key bindings left over from another class's skills.
    q += [f"DELETE FROM skills WHERE characterid = {cid} AND skillid = {NIMBLE_FEET};",
          f"INSERT INTO skills (skillid, characterid, skilllevel, masterlevel, expiration) VALUES ({NIMBLE_FEET}, {cid}, 3, 0, -1);"]
    keep = ",".join(str(sid) for sid, _, _ in skills) or "0"
    q += [f"DELETE FROM keymap WHERE characterid = {cid} AND type = 1 AND action NOT IN ({keep}, {NIMBLE_FEET});",
          # Shift gets the sprint unless the player already put something on Shift or bound the sprint elsewhere.
          f"INSERT INTO keymap (characterid, `key`, `type`, `action`) SELECT {cid}, {KEY_SHIFT}, 1, {NIMBLE_FEET} FROM DUAL "
          f"WHERE NOT EXISTS (SELECT 1 FROM keymap k WHERE k.characterid = {cid} AND k.`key` = {KEY_SHIFT}) "
          f"AND NOT EXISTS (SELECT 1 FROM keymap k WHERE k.characterid = {cid} AND k.type = 1 AND k.action = {NIMBLE_FEET});"]
    money = f", meso = {meso}" if meso is not None else ""
    q.append(f"UPDATE characters SET level = {level}, exp = 0, job = {job}, str = {stats['str']}, dex = {stats['dex']}, "
             f"`int` = {stats['int']}, luk = {stats['luk']}, ap = 0, sp = '{int(spare_sp)},0,0,0,0,0,0,0,0,0', maxhp = {hp}, hp = {hp}, "
             f"maxmp = {mp}, mp = {mp}, fame = GREATEST(fame, {fame}){money} WHERE id = {cid};")
    q.append("ROLLBACK;" if check else "COMMIT;")
    sql_run("\n".join(q))
    print("Check passed: the changes ran without errors and were undone." if check
          else "Done. A database backup was saved to Backups first.")


def write_loadouts(data):
    path = os.path.join(REF, "Loadouts.tsv")
    with io.open(path, "w", encoding="utf-8", newline="\n") as f:
        f.write("line\tlevel\tgender\tslot\titem_id\titem\treq_level\tpick\n")
        count = 0
        for line in LINES:
            for level in LEVELS:
                for gender, g in ((0, "m"), (1, "f")):
                    for slot, (item, label) in loadout(data, line, level, gender).items():
                        f.write(f"{line}\t{level}\t{g}\t{slot}\t{item['id']}\t{item['name']}\t{item['req_level']}\t{label}\n")
                        count += 1
    print(f"Loadouts.tsv: {count} rows")


def main():
    p = argparse.ArgumentParser(description="Set up a test character.")
    p.add_argument("name", nargs="?")
    p.add_argument("line", nargs="?", help="one of: " + ", ".join(LINES) + " (job names like 'hermit' also work)")
    p.add_argument("level", nargs="?", type=int)
    p.add_argument("--create", action="store_true", help="create the character by copying the template")
    p.add_argument("--template", default="trialguy", help="character to copy when creating (default trialguy)")
    p.add_argument("--gender", choices=["m", "f"], help="gender for a created character (default: the template's)")
    p.add_argument("--meso", type=int, help="set the character's meso to this amount")
    p.add_argument("--max-skills", action="store_true",
                   help="for testing: every skill of the jobs reached, at max level, ignoring skill points")
    p.add_argument("--no-skills", action="store_true", help="for testing: no class skills at all")
    p.add_argument("--sp", type=int, default=0, help="unspent skill points to leave on the character")
    p.add_argument("--dry-run", action="store_true", help="show what would be set, change nothing")
    p.add_argument("--check", action="store_true", help="run the changes against the database, then undo them")
    p.add_argument("--loadouts", action="store_true", help="rewrite Settings/Reference/Loadouts.tsv and exit")
    a = p.parse_args()
    data = Data()
    if a.loadouts:
        write_loadouts(data)
        return
    if not (a.name and a.line and a.level):
        p.error("name, line and level are required")
    line = a.line.lower().replace(" ", "").replace("/", "").replace("-", "")
    line = ALIASES.get(line, line)
    if line not in LINES:
        p.error(f"unknown line '{a.line}'")
    if not 1 <= a.level <= 200:
        p.error("level must be 1-200")
    if a.create and not a.dry_run:
        if find_character(a.name):
            raise SystemExit(f"Character '{a.name}' already exists.")
        create_character(a.name, a.template, {"m": 0, "f": 1}.get(a.gender))
    elif a.create and a.dry_run and not find_character(a.name):
        raise SystemExit("Dry run with --create: the character does not exist yet, so there is nothing to show. "
                         "Run the dry run against an existing character.")
    mode = "max" if a.max_skills else "none" if a.no_skills else "build"
    apply(data, a.name, line, a.level, a.meso, a.dry_run, a.check, mode, a.sp)


if __name__ == "__main__":
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")
    main()
