# Reference lists

Names, IDs and numbers for everything in the game, built from the server's own game data (`Server/wz`) and database. Use them to look up an ID for a GM command, a database edit or a code change.

The `.tsv` files are tab-separated text. Open them in a text editor and search, or open them in Excel.

## Names and IDs

| File | Rows | Columns |
|------|------|---------|
| [Jobs.tsv](Jobs.tsv) | 82 | id, name |
| [Skills.tsv](Skills.tsv) | 541 | id, job id, job, name, max level |
| [Maps.tsv](Maps.tsv) | 4,416 | id, area, name |
| [Mobs.tsv](Mobs.tsv) | 1,568 | id, name, level, HP, exp, boss |
| [Npcs.tsv](Npcs.tsv) | 7,075 | id, name, role |
| [Equips.tsv](Equips.tsv) | 5,116 | id, name, type, required level, job, scroll slots, cash, stats, required STR/DEX/INT/LUK/fame |
| [Items.tsv](Items.tsv) | 5,482 | id, name, kind (use, setup, etc, cash, pet), description |
| [Quests.tsv](Quests.tsv) | 2,818 | id, name, area, start NPC, level range, monsters to kill, items to collect |
| [Commands.tsv](Commands.tsv) | 184 | GM level, command, description |

## Game numbers

| File | Rows | Columns |
|------|------|---------|
| [Drops.tsv](Drops.tsv) | 22,162 | monster, item, quantity, chance in percent, quest. The last rows are drops from every monster. |
| [Shops.tsv](Shops.tsv) | 3,886 | shop, NPC, item, price |
| [Scrolls.tsv](Scrolls.tsv) | 754 | id, name, success chance, destroy chance, stats |
| [SkillDetails.tsv](SkillDetails.tsv) | 10,462 | one row per skill level: MP cost, damage, attack count, targets, duration, cooldown and more |

Drop chances are before the server's drop rate. With `drop_rate` 2, a 1% drop is 2% in play.

## Travel and loadouts

| File | What it is |
|------|------------|
| [Travel.md](Travel.md) | Every ride, taxi and tower: route, cost and time. Written by hand from the scripts. |
| [Loadouts.tsv](Loadouts.tsv) | The gear each class gets at levels 10 to 100, as picked by the character tool. See [Scripts](../Scripts/README.md). |

## Good to know

- The lists show the **server's** data. The client has its own copy; they match as long as we change both together.
- `Mobs.tsv` and `Equips.tsv` include entries that have no name. Those are usually unused or internal.
- Multi-part bosses appear as several rows (Zakum's body and arms, for example), each with its own HP.
- Max level in `Skills.tsv` is blank for a few skills whose level text is stored differently.

## Rebuilding

After editing the game data or the database, run this from the project folder, with the database running:

```
python Settings/Reference/Build-Reference.py
python Settings/Scripts/Make-Character.py --loadouts
```

They overwrite the lists. Only `Travel.md` is edited by hand.
