"""Writes the drop site: docs/drops.html and docs/drops-data.js, a searchable page of what drops where.

    python Settings/Reference/Build-Reference.py      first, so the lists match the database
    python Settings/Scripts/Make-Drop-Site.py

Run both after any change to drops. The page is made from the reference lists (Drops.tsv, Mobs.tsv,
MobSpawns.tsv, Equips.tsv, Items.tsv, Hunting-Spots.tsv) and the drop rates in Settings/config.yaml, so it
shows the chances a player really has. The look of the page is the template at the bottom of this file.
"""
import collections
import datetime
import io
import json
import os
import re

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(os.path.dirname(HERE))
REF = os.path.join(ROOT, "Settings", "Reference")
DOCS = os.path.join(ROOT, "docs")


def rows(name):
    with io.open(os.path.join(REF, name), encoding="utf-8") as f:
        head = f.readline().rstrip("\n").split("\t")
        return [dict(zip(head, line.rstrip("\n").split("\t"))) for line in f]


def rate(name):
    with io.open(os.path.join(ROOT, "Settings", "config.yaml"), encoding="utf-8") as f:
        m = re.search(r"^\s*" + name + r":\s*(\d+)", f.read(), re.M)
    return int(m.group(1)) if m else 1


def main():
    mobs = {r["id"]: r for r in rows("Mobs.tsv")}
    home = {}
    for r in rows("MobSpawns.tsv"):
        if not (r["count"].isdigit() and r["map_id"].isdigit() and r["map"]):
            continue
        rank = (int(r["map_id"]) < 900000000, int(r["count"]))          # ordinary maps before event copies
        if rank > home.get(r["mob_id"], ((False, 0), ""))[0]:
            place = r["map"].strip() + (f" ({r['area'].strip()})" if r["area"].strip() and r["area"] != r["map"] else "")
            home[r["mob_id"]] = (rank, place)
    popular = {}
    by_name = collections.defaultdict(list)
    for mob_id, m in mobs.items():
        by_name[m["name"].lower()].append(mob_id)
    for r in rows("Hunting-Spots.tsv"):
        found = [i for i in by_name.get(r["monster"].lower(), []) if i in home]
        if found:
            best = max(found, key=lambda i: home[i][0])
            popular[best] = f"{r['player_from']}-{r['player_to']}"
    equips = {r["id"]: r for r in rows("Equips.tsv")}
    items = {r["id"]: r for r in rows("Items.tsv")}
    # The same monster often exists several times (party quest and event copies). One per name is shown:
    # the copy that lives on an ordinary map in the largest number, or the first one if none does.
    shown = set()
    for name, ids in by_name.items():
        shown.add(max(ids, key=lambda i: (home.get(i, ((False, 0), ""))[0], -int(i))))

    out_mobs, out_items, drops, everywhere = {}, {}, [], []
    for d in rows("Drops.tsv"):
        if not d["item_id"].isdigit():
            continue
        item_id = d["item_id"]
        chance = round(float(d["chance_percent"] or 0) * 10000)         # parts in a million, before the drop rate
        if item_id != "0" and item_id not in out_items:
            if item_id in equips:
                e = equips[item_id]
                out_items[item_id] = [e["name"], "e", int(e["req_level"] or 0), e["type"]]
            elif item_id in items:
                i = items[item_id]
                out_items[item_id] = [i["name"], {"use": "u", "etc": "t", "setup": "s"}.get(i["kind"], "t"), 0, i["kind"]]
            else:
                continue
        low, high = int(d["min"] or 1), int(d["max"] or 1)
        quest = 1 if d["quest_id"] and d["quest_id"] != "0" else 0
        if d["mob_id"] == "all":
            everywhere.append([int(item_id), chance, low, high])
            continue
        m = mobs.get(d["mob_id"])
        if not m or not m["name"].strip() or d["mob_id"] not in shown:
            continue
        if d["mob_id"] not in out_mobs:
            out_mobs[d["mob_id"]] = [m["name"].strip(), int(m["level"] or 0), 1 if m["boss"] else 0,
                                     home.get(d["mob_id"], (0, ""))[1], popular.get(d["mob_id"], "")]
        drops.append([int(d["mob_id"]), int(item_id), chance, low, high, quest])

    data = {"made": datetime.date.today().isoformat(), "dropRate": rate("drop_rate"), "bossRate": rate("boss_drop_rate"),
            "mesoRate": rate("meso_rate"), "mobs": out_mobs, "items": out_items, "drops": drops, "everywhere": everywhere}
    os.makedirs(DOCS, exist_ok=True)
    with io.open(os.path.join(DOCS, "drops-data.js"), "w", encoding="utf-8", newline="\n") as f:
        f.write("// Made by Settings/Scripts/Make-Drop-Site.py. Do not edit by hand.\nwindow.DROPS = "
                + json.dumps(data, ensure_ascii=False, separators=(",", ":")) + ";\n")
    with io.open(os.path.join(DOCS, "drops.html"), "w", encoding="utf-8", newline="\n") as f:
        f.write(PAGE)
    print(f"{len(out_items)} items, {len(out_mobs)} monsters, {len(drops)} drops, {len(popular)} popular hunting spots.")
    print("Wrote docs/drops.html and docs/drops-data.js")


PAGE = r"""<!doctype html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>MapleStoryPlus: where it drops</title>
<style>
  :root {
    --bg: #fff7ea; --bg2: #ffe9c7; --card: #ffffff; --card2: #fff3dc; --line: #f1cf96;
    --text: #40280f; --dim: #8a6a45; --accent: #f07d00; --accent2: #3f9b2f; --boss: #d43c2c; --quest: #2b78c5;
    --hero: radial-gradient(800px 400px at 15% 0%, rgba(255, 190, 70, .65), transparent 60%),
            radial-gradient(700px 400px at 90% 10%, rgba(120, 200, 90, .45), transparent 60%), var(--bg2);
    --title: linear-gradient(180deg, #ffb02e, #f07d00 60%, #c95a00);
    --shadow: 0 5px 0 rgba(240, 125, 0, .16);
  }
  @media (prefers-color-scheme: dark) {
    :root {
      --bg: #1c130a; --bg2: #2a1a0b; --card: #2a1d10; --card2: #36260f; --line: #5c4220;
      --text: #ffeccf; --dim: #c2a57c; --accent: #ffa531; --accent2: #7ed56a; --boss: #ff7a66; --quest: #7db9f0;
      --hero: radial-gradient(800px 400px at 15% 0%, rgba(240, 125, 0, .35), transparent 60%),
              radial-gradient(700px 400px at 90% 10%, rgba(63, 155, 47, .28), transparent 60%), var(--bg2);
      --shadow: 0 5px 0 rgba(0, 0, 0, .35);
    }
  }
  * { box-sizing: border-box; }
  body { margin: 0; background: var(--bg); color: var(--text); font: 16px/1.5 "Trebuchet MS", "Segoe UI", system-ui, sans-serif; }
  a { color: var(--accent); }
  header { background: var(--hero); border-bottom: 2px solid var(--line); padding: 36px 16px 24px; text-align: center; }
  h1 { margin: 0; font-size: clamp(30px, 6vw, 46px); line-height: 1.1; background: var(--title); -webkit-background-clip: text;
       background-clip: text; color: transparent; }
  header p { margin: 8px auto 0; max-width: 60ch; color: var(--dim); }
  .bar { position: sticky; top: 0; z-index: 2; background: var(--bg); border-bottom: 2px solid var(--line); padding: 12px 16px; }
  .bar > div { max-width: 980px; margin: 0 auto; display: flex; flex-wrap: wrap; gap: 8px; align-items: center; }
  input[type=search] { flex: 1 1 260px; min-width: 0; font: inherit; color: var(--text); background: var(--card);
       border: 2px solid var(--line); border-radius: 14px; padding: 10px 14px; }
  input[type=search]:focus-visible, button:focus-visible, a:focus-visible { outline: 3px solid var(--accent); outline-offset: 2px; }
  .chip { font: inherit; font-size: 14px; color: var(--text); background: var(--card); border: 2px solid var(--line);
       border-radius: 999px; padding: 6px 13px; cursor: pointer; }
  .chip[aria-pressed=true] { background: var(--accent); border-color: var(--accent); color: #fff; }
  main { max-width: 980px; margin: 0 auto; padding: 18px 16px 60px; }
  .hint { color: var(--dim); font-size: 14px; margin: 0 0 12px; }
  .list { display: grid; gap: 8px; }
  .row { display: flex; flex-wrap: wrap; align-items: baseline; gap: 4px 10px; width: 100%; text-align: left; font: inherit;
       color: var(--text); background: var(--card); border: 2px solid var(--line); border-radius: 14px; padding: 9px 14px; cursor: pointer; }
  .row:hover { border-color: var(--accent); }
  .row b { font-weight: 700; }
  .meta { color: var(--dim); font-size: 14px; }
  .tag { font-size: 12px; border-radius: 999px; padding: 1px 8px; border: 1.5px solid currentColor; white-space: nowrap; }
  .tag.boss { color: var(--boss); } .tag.hot { color: var(--accent2); } .tag.quest { color: var(--quest); }
  .card { background: var(--card); border: 2px solid var(--line); border-radius: 22px; box-shadow: var(--shadow); padding: 18px 18px 8px; }
  .card h2 { margin: 0 0 2px; font-size: 24px; }
  .card .meta { margin: 0 0 12px; }
  .back { display: inline-block; margin: 0 0 12px; font: inherit; color: var(--accent); background: none; border: 0; padding: 0; cursor: pointer; text-decoration: underline; }
  h3 { margin: 16px 0 6px; font-size: 15px; text-transform: uppercase; letter-spacing: .04em; color: var(--dim); }
  table { width: 100%; border-collapse: collapse; }
  td { padding: 7px 6px; border-top: 1px solid var(--line); vertical-align: baseline; }
  td.n { text-align: right; white-space: nowrap; font-variant-numeric: tabular-nums; }
  td button { font: inherit; color: var(--accent); background: none; border: 0; padding: 0; cursor: pointer; text-align: left; text-decoration: underline; }
  .empty { color: var(--dim); padding: 30px 0; text-align: center; }
  footer { text-align: center; color: var(--dim); font-size: 14px; padding: 0 16px 40px; }
  @media (max-width: 560px) { td.where { display: none; } .card { padding: 14px 12px 6px; border-radius: 18px; } }
</style>
</head>
<body>
<header>
  <h1>Where it drops</h1>
  <p>Every item and every monster on MapleStoryPlus, with the chance you really have. <a href="index.html">What else is different here</a></p>
</header>
<div class="bar"><div>
  <input type="search" id="search" placeholder="Search an item or a monster..." autocomplete="off" aria-label="Search an item or a monster">
  <button class="chip" data-kind="all" aria-pressed="true">Everything</button>
  <button class="chip" data-kind="item" aria-pressed="false">Items</button>
  <button class="chip" data-kind="mob" aria-pressed="false">Monsters</button>
  <button class="chip" data-kind="hot" aria-pressed="false">Hunting spots</button>
</div></div>
<main id="main"></main>
<footer id="footer"></footer>
<script src="drops-data.js"></script>
<script>
(function () {
  var D = window.DROPS, main = document.getElementById("main"), search = document.getElementById("search"), kind = "all";
  if (!D) { main.innerHTML = '<p class="empty">The drop data did not load. Run Make-Drop-Site.py again.</p>'; return; }
  var byItem = {}, byMob = {};
  D.drops.forEach(function (d) { (byItem[d[1]] = byItem[d[1]] || []).push(d); (byMob[d[0]] = byMob[d[0]] || []).push(d); });
  var KINDS = { e: "Equipment", u: "Use items", t: "Etc items", s: "Setup items" };
  document.getElementById("footer").textContent = "Made " + D.made + " from the server's own drop table. Drop rate x" + D.dropRate +
      ", bosses x" + D.bossRate + ", mesos x" + D.mesoRate + " are counted in.";

  function esc(s) { return String(s).replace(/[&<>"]/g, function (c) { return { "&": "&amp;", "<": "&lt;", ">": "&gt;", '"': "&quot;" }[c]; }); }
  // The chance a player really has: the table's chance times the server's drop rate
  function odds(chance, boss) {
    var p = Math.min(1, chance / 1e6 * (boss ? D.bossRate : D.dropRate));
    if (p <= 0) return "never";
    if (p >= 0.995) return "always";
    return p >= 0.1 ? Math.round(p * 100) + "%" : "1 in " + Math.round(1 / p).toLocaleString("en");
  }
  function amount(d) { return d[3] === d[4] ? (d[3] > 1 ? " x" + d[3] : "") : " x" + d[3] + "-" + d[4]; }
  function mobTags(m) {
    return (m[2] ? ' <span class="tag boss">boss</span>' : "") + (m[4] ? ' <span class="tag hot">hunting spot, level ' + esc(m[4]) + "</span>" : "");
  }
  function go(hash) { location.hash = hash; }

  function showItem(id) {
    var it = D.items[id];
    if (!it) return showList();
    var list = (byItem[id] || []).slice().sort(function (a, b) {
      return b[2] * (D.mobs[b[0]][2] ? D.bossRate : D.dropRate) - a[2] * (D.mobs[a[0]][2] ? D.bossRate : D.dropRate);
    });
    var html = '<button class="back" data-go="">Back to the search</button><div class="card"><h2>' + esc(it[0]) + '</h2><p class="meta">' +
        esc(KINDS[it[1]] || "Item") + (it[1] === "e" ? ": " + esc(it[3]) + ", needs level " + it[2] : "") + "</p>";
    var any = D.everywhere.filter(function (e) { return String(e[0]) === String(id); })[0];
    if (any) html += "<p>Any monster in the game can drop this: " + odds(any[1], false) + ".</p>";
    if (list.length) {
      html += "<h3>Dropped by " + list.length + " monster" + (list.length > 1 ? "s" : "") + "</h3><table>";
      list.forEach(function (d) {
        var m = D.mobs[d[0]];
        html += '<tr><td><button data-go="mob=' + d[0] + '">' + esc(m[0]) + "</button> <span class=\"meta\">level " + m[1] + "</span>" + mobTags(m) +
            (d[5] ? ' <span class="tag quest">quest only</span>' : "") + '</td><td class="where meta">' + esc(m[3] || "") +
            '</td><td class="n">' + odds(d[2], m[2]) + "</td></tr>";
      });
      html += "</table>";
    } else if (!any) html += '<p class="meta">Nothing drops this.</p>';
    main.innerHTML = html + "</div>";
  }

  function showMob(id) {
    var m = D.mobs[id];
    if (!m) return showList();
    var list = byMob[id] || [], html = '<button class="back" data-go="">Back to the search</button><div class="card"><h2>' + esc(m[0]) +
        '</h2><p class="meta">Level ' + m[1] + (m[3] ? ", lives in " + esc(m[3]) : "") + mobTags(m) + "</p>";
    var meso = list.filter(function (d) { return d[1] === 0; })[0];
    if (meso) html += "<p>Mesos: " + (meso[3] * D.mesoRate).toLocaleString("en") + " to " + (meso[4] * D.mesoRate).toLocaleString("en") + ", " + odds(meso[2], m[2]) + ".</p>";
    ["e", "u", "t", "s"].forEach(function (k) {
      var part = list.filter(function (d) { return d[1] !== 0 && D.items[d[1]] && D.items[d[1]][1] === k; })
          .sort(function (a, b) { return k === "e" ? D.items[a[1]][2] - D.items[b[1]][2] || b[2] - a[2] : b[2] - a[2]; });
      if (!part.length) return;
      html += "<h3>" + KINDS[k] + " (" + part.length + ")</h3><table>";
      part.forEach(function (d) {
        var it = D.items[d[1]];
        html += '<tr><td><button data-go="item=' + d[1] + '">' + esc(it[0]) + "</button>" + esc(amount(d)) +
            (k === "e" ? ' <span class="meta">' + esc(it[3]) + ", level " + it[2] + "</span>" : "") +
            (d[5] ? ' <span class="tag quest">quest only</span>' : "") + '</td><td class="n">' + odds(d[2], m[2]) + "</td></tr>";
      });
      html += "</table>";
    });
    main.innerHTML = html + "</div>";
  }

  function showList() {
    var words = search.value.toLowerCase().split(/\s+/).filter(Boolean), found = [];
    var match = function (name) { name = name.toLowerCase(); return words.every(function (w) { return name.indexOf(w) >= 0; }); };
    if (kind === "hot") {
      Object.keys(D.mobs).forEach(function (id) { var m = D.mobs[id]; if (m[4] && match(m[0])) found.push(["mob", id, m[0], m[1]]); });
      found.sort(function (a, b) { return parseInt(D.mobs[a[1]][4]) - parseInt(D.mobs[b[1]][4]); });
    } else if (words.length) {
      if (kind !== "mob") Object.keys(D.items).forEach(function (id) { if (match(D.items[id][0])) found.push(["item", id, D.items[id][0], D.items[id][2]]); });
      if (kind !== "item") Object.keys(D.mobs).forEach(function (id) { if (match(D.mobs[id][0])) found.push(["mob", id, D.mobs[id][0], D.mobs[id][1]]); });
      var q = words.join(" ");
      found.sort(function (a, b) {
        var x = a[2].toLowerCase(), y = b[2].toLowerCase();
        return (x === q ? 0 : x.indexOf(q) === 0 ? 1 : 2) - (y === q ? 0 : y.indexOf(q) === 0 ? 1 : 2) || x.localeCompare(y);
      });
    }
    if (!words.length && kind !== "hot") {
      main.innerHTML = '<p class="empty">Type the name of an item or a monster. ' + Object.keys(D.items).length.toLocaleString("en") + " items and " +
          Object.keys(D.mobs).length.toLocaleString("en") + ' monsters are listed.<br>Or press "Hunting spots" for the popular places to train.</p>';
      return;
    }
    if (!found.length) { main.innerHTML = '<p class="empty">Nothing by that name drops or is dropped.</p>'; return; }
    var shown = found.slice(0, 80), html = '<p class="hint">' + found.length.toLocaleString("en") + " found" +
        (found.length > shown.length ? ", the first " + shown.length + " shown. Type more to narrow it down." : ".") + '</p><div class="list">';
    shown.forEach(function (f) {
      if (f[0] === "item") {
        var it = D.items[f[1]], n = (byItem[f[1]] || []).length;
        html += '<button class="row" data-go="item=' + f[1] + '"><b>' + esc(it[0]) + '</b><span class="meta">' + esc(it[1] === "e" ? it[3] + ", level " + it[2] : KINDS[it[1]]) +
            " &middot; " + (n ? n + " monster" + (n > 1 ? "s" : "") : "any monster") + "</span></button>";
      } else {
        var m = D.mobs[f[1]];
        html += '<button class="row" data-go="mob=' + f[1] + '"><b>' + esc(m[0]) + '</b><span class="meta">monster, level ' + m[1] + (m[3] ? " &middot; " + esc(m[3]) : "") +
            "</span>" + mobTags(m) + "</button>";
      }
    });
    main.innerHTML = html + "</div>";
  }

  function route() {
    var h = location.hash.slice(1), m = /^(item|mob)=(\d+)$/.exec(h);
    if (m && m[1] === "item") showItem(m[2]); else if (m) showMob(m[2]); else showList();
    if (m) window.scrollTo(0, 0);
  }
  main.addEventListener("click", function (e) {
    var b = e.target.closest("[data-go]");
    if (b) go(b.getAttribute("data-go"));
  });
  search.addEventListener("input", function () { if (location.hash.length > 1) go(""); else showList(); });
  Array.prototype.forEach.call(document.querySelectorAll(".chip"), function (chip) {
    chip.addEventListener("click", function () {
      kind = chip.getAttribute("data-kind");
      Array.prototype.forEach.call(document.querySelectorAll(".chip"), function (c) { c.setAttribute("aria-pressed", c === chip ? "true" : "false"); });
      if (location.hash.length > 1) go(""); else showList();
    });
  });
  window.addEventListener("hashchange", route);
  route();
})();
</script>
</body>
</html>
"""


if __name__ == "__main__":
    main()
