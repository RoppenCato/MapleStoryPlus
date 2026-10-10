# Scripts

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

### Not tested yet

The tool has only been run in check mode, where the changes are undone. No character built by it has been opened in the game.

## Bot-Chat-Bridge.py

Prototype: bots answer whispers through Claude Haiku. Started with `Start-Bot-Chat.bat` in the project folder; the window shows every exchange.

- Any bot can be whispered.
- Nothing is saved. A bot's personality is made up from its name, and the conversation is forgotten after 10 minutes of silence or when the window closes.
- Replies come from Claude Code running Haiku on your Claude login, with no API key. Run `Login-Bot-Chat.bat` once to sign it in.
- Each reply starts a new Claude Code process and takes 2 to 5 seconds.
- Bots write proper English and use common MapleStory words.
- Bots give directions: ask for the way to a town, or to a monster you were just talking about, and the bridge works out the route from the map you are on (walking, cabs and rides with fares). Follow-up questions like "where is that?" and "how do I get there?" use what the conversation was last about.
- Bots know drops and monster locations: when you name an item or monster, the bridge looks it up in `Drops.tsv` and `MobSpawns.tsv` and hands the facts to the bot. The window shows what it found on a line starting with `knows:`.
- Settings (reply length, how many lines are remembered, the personality lists) are at the top of the script.

Test without the game:

```
python Settings/Scripts/Bot-Chat-Bridge.py --say "hey, how's the hunt?"
```

Tested in the game on 2026-10-10: whispering a bot gets a reply in 2 to 4 seconds.
