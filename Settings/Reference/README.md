# Reference lists

Names and IDs for everything in the game, built from the server's own game data (`Server/wz`). Use them to look up an ID for a GM command, a database edit or a code change.

The files are tab-separated text. Open them in a text editor and search, or open them in Excel.

| File | Rows | Columns |
|------|------|---------|
| [Jobs.tsv](Jobs.tsv) | 82 | id, name |
| [Skills.tsv](Skills.tsv) | 541 | id, job id, job, name, max level |
| [Maps.tsv](Maps.tsv) | 4,416 | id, area, name |
| [Mobs.tsv](Mobs.tsv) | 1,568 | id, name, level, HP, exp, boss |
| [Npcs.tsv](Npcs.tsv) | 7,075 | id, name, role |
| [Equips.tsv](Equips.tsv) | 5,116 | id, name, type, required level, job, scroll slots, cash, stats |
| [Items.tsv](Items.tsv) | 5,482 | id, name, kind (use, setup, etc, cash, pet), description |

## Good to know

- The lists show the **server's** data. The client has its own copy; they match as long as we change both together.
- `Mobs.tsv` and `Equips.tsv` include entries that have no name. Those are usually unused or internal.
- Multi-part bosses appear as several rows (Zakum's body and arms, for example), each with its own HP.
- Max level in `Skills.tsv` is blank for a few skills whose level text is stored differently.

## Rebuilding

After editing the game data, run this from the project folder:

```
python Settings/Reference/Build-Reference.py
```

It overwrites the lists. Nothing here is edited by hand.
