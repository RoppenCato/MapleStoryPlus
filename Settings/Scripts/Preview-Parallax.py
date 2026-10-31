"""Shows how background layers slide against each other as the camera moves, without starting the game.

    python Settings/Scripts/Preview-Parallax.py --map 100000000
    python Settings/Scripts/Preview-Parallax.py --layers my-layers.tsv --span 4000

Writes parallax.png (the view at the left, middle and right of the map, one above the other) and
parallax.gif (the camera panning across) to Settings/Inspiration/_Preview, or to --out.

--map uses a real map's layers and the pictures in Settings/Inspiration/Maps/Backgrounds.
--layers uses new art: a tab-separated file with a header and the columns
    file  type  x  y  rx  ry  cx  cy  a  front  ox  oy
Only file is needed; the others default to 0 (a to 255). ox and oy are the picture's origin.
Rows are drawn from the back to the front. Paths are relative to the file.

Only the background is drawn, not the ground, objects or monsters, so hard bottom edges that the ground
would hide show here. Drifting layers stand still.
"""
import argparse
import csv
import os
import xml.etree.ElementTree as ET

from PIL import Image

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(os.path.dirname(HERE))
MAP_WZ = os.path.join(ROOT, "Server", "wz", "Map.wz")
ART = os.path.join(ROOT, "Settings", "Inspiration", "Maps", "Backgrounds")


def origin_of(bS, no, ani):
    root = ET.parse(os.path.join(MAP_WZ, "Back", bS + ".img.xml")).getroot()
    section = next(x for x in root if x.get("name") == ("ani" if ani else "back"))
    node = next(x for x in section if x.get("name") == str(no))
    canvas = node if node.tag == "canvas" else next(x for x in node if x.tag == "canvas")
    o = canvas.find("vector[@name='origin']")
    return (int(o.get("x")), int(o.get("y"))) if o is not None else (0, 0)


def map_layers(map_id):
    s = f"{map_id:09d}"
    root = ET.parse(os.path.join(MAP_WZ, "Map", "Map" + s[0], s + ".img.xml")).getroot()
    parts = {x.get("name"): x for x in root}
    info = {x.get("name"): x.get("value") for x in parts["info"]}
    bounds = None
    if "VRLeft" in info:
        bounds = (int(info["VRLeft"]), int(info["VRTop"]), int(info["VRRight"]), int(info["VRBottom"]))
    elif "foothold" in parts:
        points = [{k.get("name"): int(k.get("value")) for k in h} for layer in parts["foothold"] for group in layer for h in group]
        xs = [p[k] for p in points for k in ("x1", "x2")]
        ys = [p[k] for p in points for k in ("y1", "y2")]
        bounds = (min(xs) - 50, min(ys) - 300, max(xs) + 50, max(ys) + 150)
    layers = []
    for b in sorted(parts["back"], key=lambda x: int(x.get("name"))):
        g = {k.get("name"): k.get("value") for k in b}
        if not g.get("bS"):
            continue
        ani = g.get("ani") == "1"
        no = g.get("no", "0")
        path = os.path.join(ART, g["bS"], ("animated " if ani else "") + no + ".png")
        if not os.path.exists(path):
            continue
        ox, oy = origin_of(g["bS"], no, ani)
        layers.append(dict(file=path, ox=ox, oy=oy, **{k: int(g.get(k, 0) or 0) for k in ("type", "x", "y", "rx", "ry", "cx", "cy", "front")}, a=int(g.get("a", 255) or 255)))
    return layers, bounds


def file_layers(path):
    layers = []
    with open(path, encoding="utf-8", newline="") as f:
        for row in csv.DictReader(f, delimiter="\t"):
            layer = {k: int(row.get(k) or 0) for k in ("type", "x", "y", "rx", "ry", "cx", "cy", "front", "ox", "oy")}
            layer["a"] = int(row.get("a") or 255)
            layer["file"] = os.path.join(os.path.dirname(os.path.abspath(path)), row["file"])
            layers.append(layer)
    return layers


def draw(layers, cam_x, cam_y, width, height, cache):
    """Where a layer lands on the screen: its x, plus camera * rx / 100, measured from the screen's middle."""
    view = Image.new("RGBA", (width, height), (0, 0, 0, 255))
    for layer in sorted(layers, key=lambda v: v["front"]):
        if layer["file"] not in cache:
            cache[layer["file"]] = Image.open(layer["file"]).convert("RGBA")
        art = cache[layer["file"]]
        if layer["a"] < 255:
            art = art.copy()
            art.putalpha(art.getchannel("A").point(lambda v: v * layer["a"] // 255))
        kind = layer["type"]
        # Drifting layers use rx or ry as a speed, so in that direction they stay on the map
        shift_x = -cam_x if kind in (4, 6) else cam_x * layer["rx"] / 100
        shift_y = -cam_y if kind in (5, 7) else cam_y * layer["ry"] / 100
        x = int(layer["x"] - layer["ox"] + shift_x + width / 2)
        y = int(layer["y"] - layer["oy"] + shift_y + height / 2)
        step_x = layer["cx"] if layer["cx"] > 0 else art.width
        step_y = layer["cy"] if layer["cy"] > 0 else art.height
        xs, ys = [x], [y]
        if kind in (1, 3, 4, 6, 7):
            start = x % step_x - step_x
            xs = range(start - (art.width // step_x) * step_x, width, step_x)
        if kind in (2, 3, 5, 6, 7):
            start = y % step_y - step_y
            ys = range(start - (art.height // step_y) * step_y, height, step_y)
        for py in ys:
            for px in xs:
                view.alpha_composite(art, (max(px, 0), max(py, 0)), (max(-px, 0), max(-py, 0))) if px < width and py < height and px + art.width > 0 and py + art.height > 0 else None
    return view.convert("RGB")


def main():
    p = argparse.ArgumentParser()
    p.add_argument("--map", type=int)
    p.add_argument("--layers")
    p.add_argument("--span", type=int, default=4000, help="with --layers: how wide the map is")
    p.add_argument("--width", type=int, default=1680)
    p.add_argument("--height", type=int, default=720)
    p.add_argument("--frames", type=int, default=24)
    p.add_argument("--out", default=os.path.join(ROOT, "Settings", "Inspiration", "_Preview"))
    a = p.parse_args()
    if bool(a.map) == bool(a.layers):
        p.error("give --map or --layers")
    if a.map:
        layers, bounds = map_layers(a.map)
    else:
        layers, bounds = file_layers(a.layers), None
    if not bounds:
        bounds = (-a.span // 2, -a.height // 2, a.span // 2, a.height // 2)
    left, top, right, bottom = bounds
    cam_y = (top + bottom) // 2
    # The camera stops where the screen meets the map's edge
    low = left + a.width // 2
    high = right - a.width // 2
    if high < low:
        low = high = (left + right) // 2
    os.makedirs(a.out, exist_ok=True)
    cache = {}
    stops = [draw(layers, c, cam_y, a.width, a.height, cache) for c in (low, (low + high) // 2, high)]
    strip = Image.new("RGB", (a.width, a.height * 3 + 20), (255, 255, 255))
    for i, view in enumerate(stops):
        strip.paste(view, (0, i * (a.height + 10)))
    strip.thumbnail((1400, 2000))
    strip.save(os.path.join(a.out, "parallax.png"))
    frames = []
    for i in range(a.frames):
        c = low + (high - low) * i // max(1, a.frames - 1)
        frames.append(draw(layers, c, cam_y, a.width, a.height, cache).resize((a.width // 2, a.height // 2)))
    frames[0].save(os.path.join(a.out, "parallax.gif"), save_all=True, append_images=frames[1:] + frames[-2:0:-1], duration=80, loop=0)
    print(f"{len(layers)} layers, camera x {low} to {high}, written to {a.out}")


if __name__ == "__main__":
    main()
