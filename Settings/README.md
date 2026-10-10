# Settings

`config.yaml` in this folder is the one the server reads (when started with `Start-Server.bat`). Edit it, save, restart the server.

`Server/config.yaml` is the untouched original. It is not used; keep it to compare against the defaults.

The file is long (about 450 settings). Search for the setting name with Ctrl+F. The ones we are most likely to touch are listed below.

## Rates

At the top of the file, under `worlds:`. Only the first world (Scania) is active, because `WORLDS` is 1, so only the first block matters.

| Setting | Now | What it does |
|---------|-----|--------------|
| `exp_rate` | 2 | Exp multiplier |
| `meso_rate` | 2 | Meso multiplier |
| `drop_rate` | 2 | Drop chance multiplier |
| `boss_drop_rate` | 5 | Drop multiplier for bosses (replaces `drop_rate` for them) |
| `quest_rate` | 5 | Quest exp/meso multiplier, only if `USE_QUEST_RATE` is true |
| `travel_rate` | 10 | Boats and other rides take 1/N of the normal time |
| `fishing_rate` | 10 | Fishing success multiplier |
| `channels` | 3 | Number of channels |

Related, further down under `server:`:

| Setting | Now | What it does |
|---------|-----|--------------|
| `EQUIP_EXP_RATE` | 1.0 | Equipment levelling speed |
| `PQ_BONUS_EXP_RATE` | 0.5 | Party quest exp reward |
| `PARTY_BONUS_EXP_RATE` | 1.0 | Party exp bonus |
| `RESPAWN_INTERVAL` | 4000 | Milliseconds between monster respawns |
| `USE_ENABLE_FULL_RESPAWN` | false | Always respawn all missing monsters, regardless of player count |
| `USE_ADD_RATES_BY_LEVEL` | false | Rates increase every 20 levels |

## Custom play switches

| Setting | Now | What it does |
|---------|-----|--------------|
| `USE_PERFECT_SCROLLING` | false | Failed scrolls do not use up a slot |
| `SCROLL_CHANCE_ROLLS` | 1 | Number of tries a scroll gets to succeed |
| `USE_ENHANCED_CHSCROLL` | false | Stronger chaos scroll results |
| `CHSCROLL_STAT_RATE` | 1 | Number of stat rolls on a successful chaos scroll |
| `USE_ULTRA_NIMBLE_FEET` | false | Big speed and jump boost for beginners |
| `USE_ULTRA_RECOVERY` | false | Big recovery boost |
| `USE_ULTRA_THREE_SNAILS` | false | Big damage on Three Snails |
| `USE_PERFECT_PITCH` | false | One Perfect Pitch per level-up from level 30 |
| `USE_AUTOASSIGN_STARTERS_AP` | true | AP is auto-assigned up to level 10 |
| `USE_STARTING_AP_4` | false | Old-style 4/4/4/4 starting stats |
| `USE_COMPULSORY_AUTOPOT` | true | Pet auto-potion uses as many potions as needed |
| `USE_ITEM_SORT` | true | Inventory sort/merge button |
| `ITEM_EXPIRE_TIME` | 180000 | Milliseconds before dropped items disappear |
| `USE_MTS` | false | Maple Trading System |
| `USE_FAMILY_SYSTEM` | true | Family system |

## Accounts and login

| Setting | Now | What it does |
|---------|-----|--------------|
| `AUTOMATIC_REGISTER` | true | Logging in with a new username creates the account |
| `ENABLE_PIN` / `ENABLE_PIC` | false | Extra PIN/PIC prompts at login |
| `USE_AUTOBAN` | false | Automatic cheat detection |

## Technical (leave alone until needed)

| Setting | Now | What it does |
|---------|-----|--------------|
| `DB_HOST`, `DB_USER`, `DB_PASS` | localhost, root, empty | Database login. Matches the local MySQL as set up. |
| `HOST`, `LANHOST`, `LOCALHOST` | 127.0.0.1 | Server address. Changes when friends connect. |
| `WORLDS` | 1 | Number of active worlds |

`mysql.ini` in this folder holds the database's own settings (where the data is stored, port 3306, local connections only).

## Not in this file

Some things are not settings and need other work:

- Bot behaviour (dialogue, shop items, how many bots): data files under `Server/src/main/java/soloMapling/`.
- Monster drops, shop contents, NPC scripts: the database and `Server/scripts/`.
- Damage cap, resolution, HD: mostly the client, see [Client/README.md](../Client/README.md).
