# Scripts

## Simulate-Economy.py

Estimates what a solo player earns and spends from level 1 to 120: mesos dropped, vendor value of dropped items, potions and shop gear, for a warrior, a mage and a thief. Reads the drop tables from the database (which must be running) and changes nothing.

```
python Settings/Scripts/Simulate-Economy.py
python Settings/Scripts/Simulate-Economy.py --levels --to 31
```

| Option | What it does |
|--------|--------------|
| `--levels` | One row per level instead of per ten levels. |
| `--to N` | Stop at level N. |
| `--exp-rate`, `--meso-rate`, `--drop-rate` | Try other rates than the ones in `config.yaml`. |
| `--potion-price X` | Multiply potion prices by X. |
| `--early-meso X` | Multiply the mesos dropped by monsters under level 30 by X. |

The assumptions (how often a player is hit, MP per attack, how much is picked up) are a block of numbers at the top of the script.

## Apply-Economy-Changes.py

Applies our price and meso changes to the database, each one once (remembered in the table `plus_changes`). Stop the game server first; a backup is saved before anything changes. `--check` shows what is applied and what is not.

## Make-Fixed-Shops.py

Writes `Settings/Fixed-Shops.tsv`, the set shops in Free Market rooms 1 and 2 (scrolls, potions, stars, gear for scrolling). Prices and layout are tables at the top of the script. Run it after changing them, then restart the server.

## Simulate-Damage.py

Estimates each class's damage at set levels from the real skill numbers, the gear `Make-Character.py` gives out and the game's damage formulas. Changes nothing and does not need the database.

```
python Settings/Scripts/Simulate-Damage.py
python Settings/Scripts/Simulate-Damage.py --levels 70 119
python Settings/Scripts/Simulate-Damage.py --rules
```

`--rules` checks, per class, that a new job's attack at level 1 beats the old job's attack at max. The assumptions (attacks per second per weapon, which skill a class uses, throwing star attack) are a block at the top of the script. Monster defence, elemental weakness and scrolled gear are not counted, so use it to compare classes with each other. Run `python Settings/Reference/Build-Reference.py` first if skill numbers changed.

## Make-Character.py

Sets up a test character in one go: level, job, stats, skills, gear, potions and ammo.

Run it from the project folder. The database must be running and the character's account must be logged out.

```
python Settings/Scripts/Make-Character.py trialguy fp 50
python Settings/Scripts/Make-Character.py DevBandit bandit 60 --create
```

| Option | What it does |
|--------|--------------|
| `--create` | Creates the character first, as a copy of `trialguy` on the same account (same look and key bindings). |
| `--template NAME` | Copy a different character when creating. |
| `--gender m` or `f` | Gender of a created character. |
| `--meso N` | Set meso to this amount. Without it, meso is left alone. |
| `--max-skills` | For testing: every skill of the jobs reached, at max level, ignoring skill points. |
| `--no-skills` | For testing: no class skills at all. |
| `--sp N` | Leave N unspent skill points on the character. |
| `--dry-run` | Show what would be set. Changes nothing. |
| `--check` | Run the changes against the database and undo them. Proves they work without changing anything. |

It saves a database backup to `Backups/` before every real change.

### Lines

The second word picks the weapon line. Job names also work (`hermit`, `priest`, `sniper` and so on).

| Line | Jobs at 10 / 30 / 70 | Weapon | Extra |
|------|----------------------|--------|-------|
| `hero` | Warrior / Fighter / Crusader | Two-handed sword | |
| `paladin` | Warrior / Page / White Knight | One-handed sword | Shield |
| `darkknight` | Warrior / Spearman / Dragon Knight | Spear | |
| `fp` | Magician / F/P Wizard / F/P Mage | Wand or staff | Shield, Magic Rocks from 70 |
| `il` | Magician / I/L Wizard / I/L Mage | Wand or staff | Shield, Magic Rocks from 70 |
| `cleric` | Magician / Cleric / Priest | Wand or staff | Shield, Magic Rocks from 70 |
| `hunter` | Bowman / Hunter / Ranger | Bow | Arrows, Summoning Rocks from 70 |
| `crossbow` | Bowman / Crossbowman / Sniper | Crossbow | Arrows, Summoning Rocks from 70 |
| `assassin` | Rogue / Assassin / Hermit | Claw | Throwing stars, Summoning Rocks from 70 |
| `bandit` | Rogue / Bandit / Chief Bandit | Dagger | Shield |
| `brawler` | Pirate / Brawler / Marauder | Knuckle | |
| `gunslinger` | Pirate / Gunslinger / Outlaw | Gun | Bullets |

Magicians advance at level 8. Levels 1 to 119 work; fourth job is not supported yet.

### What it sets

- **Gear:** the highest-level normal-progression item for each slot. "Normal progression" means made for the class, sold in a shop or dropped by at least two ordinary monsters, and not a Maple, event or boss item. All picks are listed in [Loadouts.tsv](../Reference/Loadouts.tsv). The old equipped gear moves to the equip inventory.
- **Stats:** every stat the gear requires is met; the rest goes into the main stat.
- **Skills:** follows `Skill-Builds.tsv` in order, limited to the skill points the level gives.
- **HP and MP:** estimates for the class and level, not the game's exact growth.
- **Supplies:** HP and MP potions for the level, and ammo that fits the weapon.

### Files you can edit

| File | What it controls |
|------|------------------|
| `Skill-Builds.tsv` | Which skills each line takes, in priority order, and to what level. |
| `Loadout-Overrides.tsv` | Force a specific item for a line, level, gender (`m`, `f` or `any`) and slot. Use `none` as the item to leave a slot empty. |

Every character also gets the sprint (Nimble Feet) on Shift if Shift is free, and key bindings for skills the character does not have are removed. Names are limited to 12 letters or digits.

## Bot-Chat-Bridge.py

Prototype: bots answer whispers through Claude Haiku. Started with `Start-Bot-Chat.bat` in the project folder; the window shows every exchange.

- Any bot can be whispered.
- Nothing is saved. A bot's personality is made up from its name, and the conversation is forgotten after 10 minutes of silence or when the window closes.
- Replies come from Claude Code running Haiku on your Claude login, with no API key. Run `Login-Bot-Chat.bat` once to sign it in.
- Each reply starts a new Claude Code process and takes 2 to 5 seconds.
- Bots are kept away from everything personal: no tools, no connectors, no memory, no saved transcripts, and they run in an empty folder outside every project. Replies that contain an email address, a file path or a detail of the computer are dropped before they reach the game.
- Bots write proper English and use common MapleStory words.
- Small talk gets no lookup. The bridge only looks things up when the message asks for game information (drop, find, where, way and similar words), so "do you like cats?" is not answered with facts about the monster Cat.
- Bots give directions: ask for the way to a town, or to a monster you were just talking about, and the bridge works out the route from the map you are on (walking, cabs and rides with fares). Follow-up questions like "where is that?" and "how do I get there?" use what the conversation was last about.
- Bots know drops and monster locations: when you name an item or monster, the bridge looks it up in `Drops.tsv` and `MobSpawns.tsv` and hands the facts to the bot. The window shows what it found on a line starting with `knows:`.
- Settings (reply length, how many lines are remembered, the personality lists) are at the top of the script.

Test without the game:

```
python Settings/Scripts/Bot-Chat-Bridge.py --say "hey, how's the hunt?"
```

Tested in the game on 2026-10-10: whispering a bot gets a reply in 2 to 4 seconds.

## Skill changes: Apply-Skill-Changes.py and Patch-Client-Skills.ps1

Every skill number we change is one row in `Skill-Changes.tsv`: skill, field, and a small formula for the value at each level. Two tools apply the list.

| Step | Command | What it does |
|------|---------|--------------|
| 1 | `python Settings/Scripts/Apply-Skill-Changes.py` | Writes the values into the server's skill data. Restart the server afterwards. |
| 2 | `powershell -ExecutionPolicy Bypass -File Settings\Scripts\Patch-Client-Skills.ps1` | Makes the client's `Skill.wz` match the server for every listed field. The game must be closed. |

Both can be run again at any time; a second run changes nothing. Add `--check` to the first or `-CheckOnly` to the second to see what would change without writing.

What needs which step:

- **Server only (step 1):** durations, cooldowns, buff strength, speed, HP and MP costs. Confirmed in game.
- **Server and client (steps 1 and 2):** damage, number of hits, number of targets. The client works these out itself.
- **Tooltips:** step 2 also rewrites the per-level description texts in the client's `String.wz`, so they show the new numbers. A number that has no place in the original wording is added at the end where that reads naturally (for example "hits up to 4 enemies"), and otherwise left out; the tool reports how many were left out.
- **Hit boxes:** the fields `lt` and `rb` set the corners of a skill's hit box, written as `x,y`.

The client patcher always starts from the untouched original, kept as `Client\MapleStory\Skill.wz.original`, writes the patched file to a temporary folder, reads it back to check every value, and only then installs it. The same goes for `String.wz` and `String.wz.original`. To undo all client changes, copy the two `.original` files over `Skill.wz` and `String.wz`.

It uses the library from HaRepacker 4.1.0 in `Tools\HaRepacker-4.1.0` (an older release, chosen because its library can be loaded directly from PowerShell; the current release in `Tools\HaRepacker` is the program with a window, for looking inside WZ files by hand).
