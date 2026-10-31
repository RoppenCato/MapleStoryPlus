# Using this art as inspiration

For a Claude making art for **a new, original game**. That game is not MapleStory and is not connected to it. This folder holds art from MapleStory (version 83), kept as a reference for how a well-loved 2D side-scroller builds its look: its proportions, motion, tiles, layered backgrounds and parallax.

## The rule: learn from it, make your own

**Nothing in this folder may go into the new game.** It is MapleStory's art and it isn't ours. Do not trace, recolour, edit, crop or assemble these files, and do not feed them to a tool to produce look-alikes. Every piece in the new game has to be drawn from scratch. If you are asked to reuse something from here, say that it can't ship and offer to make an original instead.

| Take from here | Leave here |
|---|---|
| How things are built: layers, tile grids, frame counts, timing | The pictures themselves |
| Proportions: how big things are next to the player | Its characters and monsters, such as a mushroom with a face or a slime with an antenna |
| What makes it work: readable silhouettes, strong hit poses, squash and stretch | Its signature look as a whole, so the new game shouldn't be mistaken for it |
| How colour sets a mood and separates near from far | An area's exact colours, used all together |
| The kinds of place that work, such as a sky town or a toy world | Its named places, logos, signs, buildings and layouts |

A useful test: if a player could say "that's the MapleStory one", redesign it. Ask what the new game's own world is, and let that lead. Use this folder to answer "how is this done?", not "what should this look like?"

Where the new game's own style, resolution or engine differ from what is here, follow the new game. **The numbers are a tested starting point, not requirements.** Proportions and timings carry over well; exact pixel sizes only do if the new game has a similar resolution.

Paths below are relative to this folder, unless they start with `Settings/`, which is relative to the MapleStoryPlus project, `C:\dev\MapleStoryPlus`. Run its commands from there. Keep the new game's files out of this folder and out of that project. Never commit anything from this folder except this file: the repository is public. `Settings/Scripts/Export-Inspiration.ps1` recreates the pictures if they go missing.

All numbers below were measured from the game's data (the median is the typical value). "p90" means 90% of the art is at or below that number.

## Where to look

| You are making | Look first at | Then at |
|---|---|---|
| A monster | `Monsters/Sheets/Level ... .png` for its level | `Monsters/Animations/` for motion, `Maps/Places/` to see it in its home |
| A boss | `Monsters/Sheets/Bosses part N.png` | `Monsters/Animations/` (Mano, King Slime, Mushmom, Papulatus, Pianus, Pink Bean, Crimson Balrog) |
| A whole new area | `Maps/Places/` for the closest mood | The sets for that mood in the table below |
| A background | `Maps/Backgrounds/_Overview/<set>.png` and the parallax section below | `Maps/Places/` to see the layers stacked |
| Ground or platforms | `Maps/Tiles/_Overview/<set>.png` | `Maps/Places/` to see the pieces joined |
| Houses, trees, props | `Maps/Objects/_Overview/<set>.png` | The single files in `Maps/Objects/<set>/` |
| A colour palette | The palette column below | Sample a picture in `Maps/Places/` |

Open the overview sheets first. There are about 20,000 files, and the sheets show a set at a glance. Large sets are split into `<set> part 1.png`, `part 2.png` and so on. Sheets scale big pieces down to fit, so check real sizes in the single files.

### What the folder holds

- `Maps/Places/`: 61 whole maps drawn as one picture, with their monsters.
- `Maps/Backgrounds/<set>/`: `N.png` is a still layer, `animated N.png` is the first frame of a moving one.
- `Maps/Tiles/<set>/`: `<piece> N.png`, for example `bsc 0.png`.
- `Maps/Objects/<set>/`: first frame only, named by the game's own groups, for example `grassySoil nature 3.png`.
- `Monsters/All/<Name>.png`: one standing picture per monster.
- `Monsters/Sheets/`: monsters side by side per ten levels, labelled with their level. It includes test and placeholder monsters such as "Sealed" and "Transparent Mob"; ignore those, and the odd level bands at 991 and 1791.
- `Monsters/Animations/<Name>.png`: 35 monsters, one row per action, up to 14 frames per row.

**In `Maps/Places`, these are not part of the art:**
- Black areas are where the game draws nothing, usually outside what the camera can reach.
- Layers are drawn as seen with the camera in the middle of the map, so far layers can sit a little differently in play.
- NPCs are missing, and animated pieces show their first frame.

## Places and their art

Use this to go from a mood to the right sets. Palettes are the commonest colours in the finished map, most common first, so they can include black from undrawn areas.

| Mood | Places | Background sets | Tile sets | Object sets | Palette |
|---|---|---|---|---|---|
| Sunny meadow town | Henesys, Amherst, Free Market | grassySoil | woodMarble | acc1, houseGS, door | `#3366cc #c5c4ba #8fa5a1 #4d4943` |
| Grassy fields | Forest West of Henesys, Snail Hunting Ground II | midForest | grassySoil | acc1, guide | `#429eff #4c451e #9fbb9c #697f67` |
| Lush magic forest | Ellinia, Monkey Forest I, Forest of Wisdom | shineWood | woodBridge | acc2, houseSW | `#22440f #5ba55f #a5c0a1 #206c20` |
| Dry canyon | Perion, West Rocky Mountain I | dryRock | dryRock | acc1, houseDR | `#5286ef #d0b699 #73573e #ac8661` |
| Dusk city | Kerning City, Construction Site | sunsetCity, metroCity | brownBrick, holeBrick | acc2, houseMC | `#84593a #382628 #b29679 #002f62` |
| Underground, subway | Line 1 Area 1 | metroSubway, metroSubway2 | rustSubway, graySubway | dungeon, acc2 | `#49423c #100b08 #504c44 #272728` |
| Caves | Ant Tunnel I, Cave of Evil Eye I | darkCave | darkCave, deepCave | dungeon | `#000000 #472d0b #997423 #100905` |
| Gloomy village | Sleepywood | darkWood | darkWood | acc1, houseDW | `#1d170a #4f441c #2b270f #7c7e35` |
| Mine | Dead Mine I | deepMine | deepMine | dungeon2 | `#41413b #21231f #655735 #929795` |
| Harbour | Lith Harbor, Southperry, Nautilus | vicportTown, portTown, nautilusPort | whiteMarble, blackTile | acc2, housePT, acc9 | `#425878 #5389a3 #50c6e3 #bbb9a9` |
| Beach | Florina Beach | sandBeach | woodSand | acc2, acc1 | `#1567ff #dae3d2 #484b49 #98a894` |
| Sky town | Orbis | skyStation | dryRock2, pastelBrick | acc3, houseSS | `#0f3b9e #c0beb3 #6e7d91 #3d4473` |
| Snow | El Nath, The Chilly Hill | snowyLightrock | snowyLightrock, snowyLightrock2 | acc3, houseSLR | `#b8bede #7d97a3 #55696f #cbd3de` |
| Snowy village | Rien, Snow-covered Field 1 | Rien | snowyRord | acc12, houseRI | `#159bd0 #a29d7d #dae4e3 #eef9fc` |
| Toy world | Ludibrium, Toy Factory | toyCastle, toyCastleB23 | yellowToyCastle, blueToyCastle, blankTower | acc4, houseTC | `#3552d2 #c3cb7f #703669 #59609d` |
| Warped time | Crossroad of Time, Papulatus | toyCastleB23, toyCastleDungeon | darkpurpleToyCastle | acc4, dungeon2 | `#11112d #1a016d #253356 #809d9c` |
| Alien base | Omega Sector, Kulan Field I | omegaSector | omegaSectorTown, omegaSectorField | acc4, houseOS | `#3b54bf #5f3e25 #98be8f #313641` |
| Folk village, night mountain | Korean Folk Town, Black Mountain | folkvillige, darkMountain | folkvillige, darkMountain | acc6, houseFV | `#007dfe #918c51 #4d4928 #adc8ab` |
| Underwater | Aquarium, Blue Seaweed Road, Deep Sea Gorge I | aquaRoad, aquaRoad2, aquaRoad3 | sandySeaFloor, greensandySeaFloor | acc5, houseAR | `#012f46 #17889e #24b5c9 #55f8df` |
| Dragon highland | Leafre, The Dragon Canyon | minar, dragonValley, dragonRoad | minar, dragonRoad | acc6, houseLF, dungeon3 | `#03b7f0 #515a34 #ad9a6b #97ce9d` |
| East Asian mountain | Mu Lung, Herb Town | mureung, backcho | classicBlock, mureung | acc7, houseMR, houseBC | `#695341 #5698bf #d9c9ba #9dae94` |
| Desert | Ariant, Desert of Red Sand | desert | dayDesert, nightDesert | acc8, houseAA | `#ffdc2d #823112 #c37c31 #e7be66` |
| Night steam city | Magatia | nightDesert | magatia | houseMG, acc8 | `#555f9d #11131a #1d2033 #81818d` |
| Ancient temple | Temple of Time, Road of Regrets, Pink Bean | timeTemple | (objects only) | acc10 | `#685f3d #87876b #55c2c1 #c6c19d` |
| Fairy-tale sanctuary | Ereve | ereb | fallenLeaves | acc11, acc6 | `#9b844e #84b9b0 #e1c480 #f0e596` |
| Modern city | New Leaf City | ThemeBack1, ThemeBack2 | ThemeGL2 | ThemeGL, houseGL | `#2e61b8 #5a89d0 #bfc0b5 #c6e1f7` |
| Haunted, red forest | Bent Tree, Valley of Heroes 1 | masteriaGL | halloweenoutside, masteriaGL | masteriaGL1, trap | `#331111 #7f4024 #551e0d #240d0d` |
| Wedding, pastel | Amoria | WeddingGL | woodMarble | WeddingGL, houseWGL | `#3fbff8 #8ae5f9 #caf2f4 #eafdff` |
| Lava boss room | Zakum Altar | moltenRock | moltenRock | dungeon2 | `#743a2d #d63c17 #ac2314 #f69b1a` |

### Object sets by type

- `acc1` to `acc12`: nature and props per region, in groups such as `grassySoil nature` and `dryRock rock`. acc1 is Henesys, Perion and Sleepywood; acc2 Ellinia, Kerning and Lith Harbor; acc3 Orbis and El Nath; acc4 Ludibrium and Omega; acc5 underwater; acc6 Leafre and Korean Folk Town; acc7 Mu Lung and Herb Town; acc8 Ariant and Magatia; acc9 Nautilus; acc10 Temple of Time; acc11 Ereve; acc12 Rien.
- `houseXX` and `insideXX`: buildings and interiors per town.
- `connect`: ladders and ropes. `door`: doors and windows. `guide`, `signboard`: signs, arrows and boards.
- `dungeon` to `dungeon4`: cave and underground dressing. `trap`: hazards such as fire, ice and lasers. `prop`, `vehicle`, `shop`: general props.

## The style

- **Painted, not pixel art.** Soft shading and many colours: a monster has about 60 colours, a tile about 80. Do not limit the palette or dither.
- **Crisp sprite edges.** Monster sprites are normally fully opaque with hard edges: half of them have no semi-transparent pixels at all. Semi-transparency is for glows and effects (the top tenth run about 37%), and it is common in backgrounds.
- **Dark outlines.** Characters and monsters have a thin, dark outline, and about a fifth of a monster's pixels are dark. This separates them from busy backgrounds.
- **Cute and chunky.** Big heads, simple faces with large eyes, rounded shapes and readable silhouettes. Even scary monsters stay a little comic. Features are exaggerated: an Orange Mushroom's whole face changes when hit.
- **Saturated foreground, softer background.** Near art is bright and outlined; far layers are lighter, hazier and have no hard outlines, so play stays readable.
- **Light from above,** with highlights on top and darker undersides. Ground has a bright grassy or stony top edge above a darker body.
- **Each area has one clear idea and palette.** Pick the mood first and keep every piece to it.

**Draw at real size.** MapleStory shows one image pixel as one screen pixel, so its art never looks blurred. If the new game does the same, never draw large and shrink without checking that detail survives. Save as PNG with transparency.

This describes MapleStory. Use it to see what works, and decide what the new game's own style keeps or changes.

## Scale

A player character stands about 65 pixels tall and 40 wide: a 21×31 body under a 39×35 head, so the head is half the height. Everything below is sized against this. For the new game, carry over the ratios, not the pixels:

| Thing | Next to the player |
|---|---|
| Typical monster up to level 60 | About as tall as the player |
| Typical monster around level 100 | About twice as tall |
| Typical boss | About twice as tall and four times as wide |
| Biggest boss | About 8 to 9 times as tall |
| One row of ground tile (60 pixels) | About the player's height |
| Typical decoration | About 1.5 times as tall |

## How monsters are made

Monster levels below are MapleStory's, from 1 up to about 120. Read them as "early game" through "late game".

### Size

| Monster level | Typical standing size (w × h) | Largest tenth from |
|---|---|---|
| 1–30 | 64 × 58 | 181 × 156 |
| 31–60 | 71 × 66 | 141 × 125 |
| 61–90 | 104 × 99 | 161 × 163 |
| 91–120 | 112 × 140 | 177 × 197 |
| Bosses | 152 × 142 | 310 × 311, biggest 827 × 561 |

Starter monsters such as the Snail are well under the player's height, and by about level 100 monsters tower over them. These sizes are the first `stand` frame, including any effects drawn in it.

### Actions and frames

A monster is a set of named actions, each a list of frames shown in order. Most monsters have `stand`, `move`, `hit1` and `die1`. About half also have an attack.

| Action | Typical frames | Common range | Time per frame | What it shows |
|---|---|---|---|---|
| `stand` | 6 | 1–12 | 130 ms | Idle: gentle bob or breathing, looped. Simple monsters use 2–3 frames |
| `move` | 6 | 3–8 | 140 ms | Walk or hop, looped |
| `fly` | 5 | 2–8 | 120 ms | Replaces `stand` and `move` on flyers |
| `jump` | 1 | 1 | held | One pose in the air |
| `hit1` | 1 | 1 | 600 ms | One strong pose: recoil, shock, pieces knocked loose |
| `die1` | 8 | 3–15 | 150 ms | Collapse, squash or crumble, fading out at the end |
| `attack1`, `attack2` | 12–15 | 6–23 | 120 ms | Windup, strike with a flash or lunge, recovery |
| `skill1` | 12 | 5–18 | 120 ms | Charging up and releasing, usually a glow on an unmoving body |

The bigger actions can add more: `attack3`, `skill2`, `regen` and `die2` exist, but few monsters use them.

### What makes the motion good

Open these in `Monsters/Animations/`:
- `Slime.png`: squash and stretch. It flattens, leaps long and thin, and melts away when it dies.
- `Orange Mushroom.png`: a lot of character from few frames, with a strong expression on `hit1`.
- `Stone Golem.png`: `hit1` knocks the body parts apart, `skill1` is a glow that builds and fades on a still body, and `die1` falls into a heap.
- `Mano.png` and `Mushmom.png`: boss weight, at the low end.

Rules worth keeping:
- Make `hit1` the most exaggerated pose. It is seen most, and held longest.
- Change the silhouette between frames; shading changes alone don't read at this size.
- Let attached parts follow late, like the Slime's antenna.
- Keep the feet at the same height across frames, unless the monster is leaving the ground.

### Technical rules

Each frame carries:
- `origin`: the point placed at the monster's position. Put it **at the feet, horizontally centred**: normally x about half the width, y equal to the image height.
- `delay`: time on screen in milliseconds.
- `lt` and `rb`: the body's hit box, relative to the origin. For example `lt (-27,-43)` and `rb (24,0)`.
- `head`: the top of the head, used for placing things above it, for example `(3,-43)`.
- `a0` and `a1` (optional): opacity at the frame's start and end, 0 to 255, for example to fade out at the end of `die1`. About three in four monsters use them somewhere.

Frames can differ in size, so a frame only needs to be as big as its contents; the origin keeps the feet still. **Draw monsters facing left.** The game flips them to face right.

## How tiles work

Ground is built from pieces on a **90 × 60 pixel grid**, and a set has these same pieces:

| Piece | What it is | Usual size | Origin |
|---|---|---|---|
| `bsc` | Body of the ground; must repeat seamlessly in all directions | 90 × 60 | Top left |
| `enH0` | Top surface, such as the grass, sitting above the grid line | 90 × 15–46 | Bottom left |
| `enH1` | Underside edge, hanging below the grid line | 90 × 15–25 | Top left |
| `enV0`, `enV1` | Left and right side edges | 15–33 × 60 | `enV0` top right, `enV1` top left |
| `edU`, `edD` | Rounded end caps at the top and bottom corners | about 50 × 30 | Varies |
| `slLU`, `slRU` | Slopes going up to the left or right, top surface | 90 × 75–99 | Bottom corner |
| `slLD`, `slRD` | Slopes, underside | 90 × 74–87 | Top corner |

Make these so that:
- `bsc` and each edge repeat without seams: left side matches right side at the same height on every variant.
- A set has several variants of the main pieces (commonly 6 `bsc`, 3 `enH0`, 3 `enH1`, 2 `enV0` and 1 `edU`), so long ground doesn't look stamped.
- Drawing order is `edU`/`edD` first, then `enH` and slopes, `enV`, and `bsc` last on top (`z` is -4, -3, -2 and 0). Edge pieces can therefore tuck under the body.
- A slope rises about one grid step (60 pixels) over its 90 width, so it joins the flat `enH0` on each side. Compare `slLU` and `enH0` in `Maps/Tiles/grassySoil/`: the slope is 94 tall and the flat top 38.
- The ground has to be walkable separately. The floor is a line stored in the map ("foothold"), not the art. In Henesys the main ground's grid line is at y 480 and the player walks at y 454, 26 pixels above it. Its `enH0` pieces are up to 33 tall, so the feet stand about 7 pixels into the top edge. Design the top edge with that in mind.

See `Maps/Tiles/_Overview/grassySoil.png`, then find those joins in `Maps/Places/Henesys.png`.

## How backgrounds work

A background is not one picture. It is a stack of separate layers: the maps in `Maps/Places` use 3 to 49, and the most in the game is 132. Small indoor maps may use one or none. `Maps/Backgrounds/_Overview/grassySoil.png` shows the kit for Henesys: a flat blue, a cloud band, hills, and a far tree.

Build one from the back to the front:
1. Flat colour or gradient, tiled to fill the screen. It can be a small image.
2. Far scenery such as sky, clouds or distant skyline, tiled sideways. Must repeat seamlessly.
3. Mid scenery such as hills and tree lines, with a transparent top.
4. Single accents such as one big tree, placed once.
5. Optional overlays such as light shafts, in front of everything (`front` = 1). About 1 in 10 layers does this. Keep them subtle because they cover the player.

Layer sizes vary widely: typically 287 × 226, and up to 800 × 537 for the largest tenth. A flat colour can be far smaller.

**Each layer in a MapleStory map has these settings.** The new game's engine will have its own names for most of them:

| Setting | What it does |
|---|---|
| `type` | 0 single picture; 1 repeats sideways; 2 repeats up and down; 3 repeats both ways; 4 repeats sideways and drifts sideways (clouds); 5 repeats up and down and drifts vertically (rain, bubbles); 6 and 7 repeat both ways and drift |
| `rx`, `ry` | Parallax: how the layer follows the camera, from 0 (far) to -100 (near). See the next section. On drifting types, it is the drift speed in that direction instead |
| `cx`, `cy` | Spacing when repeating; 0 uses the image's size |
| `a` | Opacity, 0–255. Nearly all layers are 255 |
| `front` | 1 draws the layer over the characters |
| `ani` | 1 uses an animated layer |
| `f` | 1 flips the picture |

Rules that follow from that:
- **Know the screen size first.** MapleStory was made for 800 × 600. The new game's resolution decides how much of each layer shows at once, so far layers should repeat sideways, and a single picture needs placing so that nothing behind it shows as a gap.
- **Map sizes:** typically 990 × 850, the widest tenth 2,315+, the biggest 9,720. Layers near the map's speed must cover all of it.
- **Keep contrast low in the back.** Layers are hazier and lighter the further they are.
- **Moving layers:** about 1 in 7 layers in maps is animated, typically with 2 frames (9 or fewer for most) and 250 ms a frame. Delays of up to 3,000 ms are normal for slow changes.

## Parallax: how the depth is made

Parallax is the game's main trick for depth. When the player walks, the camera moves, and layers slide at different speeds: far mountains barely move, near trees move almost with the ground. Nothing is drawn in 3D, but the map looks deep. Plan it from the start, because it decides how the layers are cut, sized and painted.

### The numbers

`rx` is sideways and `ry` is up and down. For layers that don't drift:

```
screen x = x - origin x + camera x * rx / 100 + screen width / 2
screen y = y - origin y + camera y * ry / 100 + screen height / 2
```

`camera` is the world position at the middle of the screen. These are MapleStory's own numbers. **In the new game's engine, use a scroll factor,** which is the same idea from 0 to 1 (for example `motion_scale` in Godot). The factor is `-rx / 100`:

```
layer screen x = layer x - camera x * factor
```

| Factor | `rx` | As the camera moves 100 pixels, on screen the layer moves | Feels like |
|---|---|---|---|
| 0 | 0 | Not at all, while the ground moves 100 | Sky or a far distance, at infinity |
| 0.05–0.2 | -5 to -20 | 5–20 | Far mountains and skyline |
| 0.3–0.5 | -30 to -50 | 30–50 | Middle distance, hills |
| 0.6–0.8 | -60 to -80 | 60–80 | Near scenery |
| 1 | -100 | 100, locked to the ground | Scenery standing right behind the platforms |

The ground, objects and monsters all move as -100. Across the game, layers go in this order: the median `rx` is -5 for the backmost fifth of a map's stack, then -30, -50, -60 and -60 at the front.

### How real maps do it

- **Henesys, the simplest good example (8 layers).** `rx` is 0 for the flat blue, -20 for the far hill and big tree, and -40 for the near meadow, with one drifting cloud layer. Four 1024-wide pieces make up the meadow, using two pictures in turn.
- **Kerning City, only 3 layers.** Sky -5, far skyline -10, near skyline -15. All are far away and tile sideways, with buildings placed as objects on top.
- **Leafre, a richer one.** Sky 0; horizon -5; drifting clouds at speeds 5–10; distant trees -30; trees -50, then -70; and near trees -100 repeating every 1650 pixels. Light shafts are in front at -80.
- **Ellinia, a tall map (44 layers).** The depth is built from many small pieces, with near values like -33, -38 and -40 and many at -100. Forest trunks at -8, -11, -13 and -15 are slightly different on purpose, so that they drift past one another and nothing looks like a single sheet.

To watch these move, run:

```
python Settings/Scripts/Preview-Parallax.py --map 240000000
```

### Making a parallax background

1. **Pick the depth planes.** Three to five planes are enough for most maps. Assign each one an `rx` with clear gaps between them, because layers with nearly the same value read as one flat sheet.
2. **Paint each plane for its distance.** Far planes are paler, hazier, less saturated, low in contrast and low in detail, with soft or no outlines. Near planes are saturated, with more contrast and sharper shapes. Shift the far planes towards the sky colour. Things that are further away should look smaller too.
3. **Cut each plane out with transparency.** Each layer shows the one behind it through its top. Give it an irregular upper edge, such as a treeline or ridge, and make gaps worth looking through.
4. **Work out how wide it must be.** A layer slides less than the camera, so it doesn't need to be as wide as the map:

   ```
   width needed = screen width + (map width - screen width) * |rx| / 100
   ```

   This is why a far layer can be small. On a 1680-wide screen, Henesys (7,466 wide) needs 3,994 at `rx` -40, and its four meadow pieces give 4,096. An `rx` of -100 needs the whole map. Either repeat the layer (`type` 1 or 3, needing a seamless join) or make it wide enough. A layer at `rx` 0 needs only the screen.
5. **Place it.** To have a layer's origin in the middle of the screen when the camera is at world position `C`, set `x = -C * rx / 100`. Do this for the moment that matters, usually the map's centre or the town's main spot. Use the same idea for `y`.
6. **Choose `ry` for the map's shape.** On a wide, flat map, keep `ry` small (Henesys: -5 to 3), so the horizon stays put behind the ground. On a tall map, use about the same value as `rx` (Ellinia, Leafre), because the player climbs and the layers must follow, or the layers run out.
7. **Add life.** Clouds use `type` 4, where `rx` becomes a speed, usually 1–10, and its sign sets the direction; `ry` still works as parallax. Sideways, such a layer is locked to the ground as well as drifting, so it can pass quickly when the player runs. In your own engine you can combine both: a low scroll factor plus a slow drift keeps clouds feeling far away.
8. **Hide the seams.** Accents that repeat, such as big trees, need wide spacing (`cx` 300–1650), and two or three different pictures in turn.
9. **Add a foreground, sparingly.** Use `front` = 1 for light shafts or mist (Leafre uses `rx` -80). It covers the player, so keep it translucent or at the screen's edges.
10. **Preview it.** Write the layers to a file and run this, then look at `Settings/Inspiration/_Preview/parallax.png`, which shows the left, middle and right of the map, and `parallax.gif`, which pans across:

    ```
    python Settings/Scripts/Preview-Parallax.py --layers my-layers.tsv --span 4000
    ```

    The file's columns are `file type x y rx ry cx cy a front ox oy`, listed from back to front, using `rx` = -100 × your scroll factor. `file` can be the path to the new game's art, and the preview doesn't change or copy it. `--span` is the map's width. Set the screen with `--width` and `--height`, which default to 1680 × 720, and send the output elsewhere with `--out`.

### What goes wrong

- **Gaps:** a layer's edge slides into view at the far ends of the map. Check both ends in the preview, and use the width formula.
- **Hard bottom edges:** most layers end in a straight line that the ground is meant to hide. If a low platform leaves it visible, extend the layer down or raise it. The preview has no ground, so these edges show there even when they are fine in play.
- **Order and speed disagree:** a layer drawn in front must move faster than the layers behind it. Otherwise the depth looks wrong and the eye notices.
- **Flat stacks:** all layers at about the same `rx`. Spread them out.
- **Busy backgrounds:** high-contrast detail behind the platforms makes monsters and the player hard to see. Save strong detail for the top half and the sides.
- **Wrong screen size:** a wider screen shows more of each layer at once. Test at the new game's real resolution, and at any others it supports. The real maps here can show gaps at 1680 wide, because they were made for 800 × 600.

These formulas follow how open-source MapleStory clients read these values, and real maps line up correctly when drawn this way, but they weren't checked in the running game. That doesn't matter for the new game: the scroll factor is the part to reuse, and your engine sets the rest. Judge it by eye in the new game.

## How objects work

Objects are pieces placed freely on the map: trees, houses, signs, lamps and grass.

- **Size:** typically 123 × 101, and up to 422 × 334 for the largest tenth. Houses and big trees run larger.
- **Origin:** usually at the centre of the picture, not at its base (in `acc1` and `houseGS`, nearly all sit at half the height). So a map places an object by its middle: work out where its base lands, and line that up with the walking line.
- **Animation:** about 1 in 8 is animated, typically 150 ms a frame (lamps, water, flags). Few frames are enough. Slow idle pieces hold for up to 1,800 ms. Only the first frame is exported.
- **Depth:** maps have 8 layers (0–7), each drawing objects, then tiles. Objects also have a `z` for order within a layer, so bushes can sit in front of the ground and houses behind.
- **Build in kits.** Each town has a house set with `basic` and `deco` parts. Make several small props per large one, because maps get their richness from many small pieces. See `Maps/Places/Henesys.png`, which is mostly reusable props from `acc1` and `houseGS`.

## Before you hand art over

1. Put it next to the new game's character for scale. Compare it with similar pieces here to check the proportions and motion, not to match the look.
2. Check it on the actual background of its map, because outlines and colours behave differently on busy art.
3. Check that it's original: nobody should recognise it as a particular MapleStory monster, building or place, and no file from here went into making it.
4. For tiles and repeating layers, tile them 3 × 3 and look for seams.
5. For animation, play it at the real delays. Motion that looks fine in a row of frames can jitter in play, usually from a moving origin.
6. Give the user the art with its data (origin, delay, hit box, repeat type, scroll factor), in the form the new game's engine needs.
