# Guide: how MapleStoryPlus is put together and how to change it

This is the practical guide. It covers how the project was set up from nothing, how to run it, and how to make each kind of change. It is kept up to date as the project changes.

For what was decided and why, see the [Development log](Development-Log.md). For the class design, see [Class changes](Class-Changes.md).

Last updated: 2026-10-11.

## Contents

1. [The pieces](#1-the-pieces)
2. [Setting it up from nothing](#2-setting-it-up-from-nothing)
3. [Running it day to day](#3-running-it-day-to-day)
4. [Who decides what: server or client](#4-who-decides-what-server-or-client)
5. [How to change things](#5-how-to-change-things)
6. [Test accounts and characters](#6-test-accounts-and-characters)
7. [Saving your work](#7-saving-your-work)
8. [Pitfalls we already hit](#8-pitfalls-we-already-hit)
9. [Where things are written down](#9-where-things-are-written-down)

## 1. The pieces

| Piece | Where | What it is |
|-------|-------|------------|
| Game server | `Server/` | A copy of [SoloMapling](https://github.com/MadaraGameDev/SoloMapling): the Cosmic v83 server (Java) plus about 3,100 bots that fill the world. |
| Server game data | `Server/wz/` | Skills, monsters, maps and items as XML files. The server reads these at start. |
| Server scripts | `Server/scripts/` | NPCs, portals, events and quests as JavaScript. NPC scripts are read each time the NPC is clicked. |
| Database | `Database/` | MySQL data: accounts, characters, inventories, drops, shops. This is the save file. |
| Game client | `Client/MapleStory/` | The original v83 game, with the MapleEzorsia v2 file `dinput8.dll` added for HD and connecting to our server. It has its own copy of the game data as `.wz` files. |
| Settings | `Settings/config.yaml` | Rates and gameplay switches. The server reads this file. |
| Our tools | `Settings/Scripts/`, `Settings/Reference/` | Scripts for skill changes, test characters, the bot chat, and lists of every ID in the game. |
| Programs | `Tools/` | Java 21, MySQL 8.4 and the WZ library, unpacked here. Nothing is installed on Windows. |

The server and the client each have their own copy of the game data. Most trouble comes from changing one and forgetting the other; section 4 says which copy matters for what.

## 2. Setting it up from nothing

These are the steps that were done, in order. The PC had no admin rights for installers, so everything is unpacked into the project folder. The paths assume `C:\dev\MapleStoryPlus`; `Settings/mysql.ini` contains that path and must be edited if the folder is somewhere else.

### 2.1 Programs

| Program | Version used | Goes in | Notes |
|---------|--------------|---------|-------|
| Java | Amazon Corretto 21.0.12 (zip) | `Tools/java21` | The server needs Java 21. |
| MySQL | 8.4.11 (zip, "no installer") | `Tools/mysql` | Not installed as a Windows service. |
| Python | 3.x | Installed normally | For our scripts. They use only what comes with Python. |
| Git | Any recent | Installed normally | |
| HaRepacker | 4.1.0 release | `Tools/HaRepacker-4.1.0` | Only `AnyCPU/MapleLib.dll` is used, to edit the client's `.wz` files. The newest HaRepacker is a single file with no separate library, which is why the old release is used. |

### 2.2 The code

1. Create the project folder and make it a git repository on branch `main`.
2. Add the original server as the remote `upstream` and disable pushing to it, so nothing of ours can end up there:
   ```
   git remote add upstream https://github.com/MadaraGameDev/SoloMapling
   git remote set-url --push upstream DISABLED
   ```
3. Merge it in under `Server/` (a subtree merge, so its history is kept).
4. Add your own GitHub repository as `origin`. Ours is public, so nothing private goes into it.
5. `.gitignore` keeps out `Tools/`, `Database/`, `Backups/`, `Client/MapleStory/` and `Client/Downloads/`.

To pull in later updates from the original:

```
git fetch upstream
git merge -X subtree=Server upstream/main
```

After such a merge, check every file in the "Changes to the server code" table of the Development log.

### 2.3 The database

1. Write `Settings/mysql.ini`: program folder, data folder `Database/`, port 3306, `bind-address=127.0.0.1` (this PC only).
2. Create the data folder once: `Tools\mysql\bin\mysqld --defaults-file=Settings\mysql.ini --initialize-insecure`. This gives the user `root` an empty password.
3. Start the database and create an empty database named `cosmic`. The server creates all tables itself on its first start.

Set a real database password before anyone else connects.

### 2.4 The server

1. Copy `Server/config.yaml` to `Settings/config.yaml`. The copy is the one in use; the original stays as a reference.
2. A small code change lets the server read a settings file from another place (`-Dconfig-path=...`).
3. Build: run `Build-Server.bat`. The result is `Server/target/Cosmic.jar`.
4. Start: run `Start-Server.bat`. It starts the database if needed, then the server. The server is ready when the window says `Cosmic is now online`.

### 2.5 The client

1. Download the v83 installer and the matching game data from [P0nk/Cosmic-client](https://github.com/P0nk/Cosmic-client), and `dinput8.dll` with its `config.ini` from the [MapleEzorsia v2 releases](https://github.com/444Ro666/MapleEzorsia-v2/releases) (Release 2). Only download Ezorsia from the author's own page.
2. Install the game into `Client/MapleStory/`.
3. Replace its `.wz` files with the ones from `cosmic-wz`, so client and server data match.
4. Put `dinput8.dll`, `config.ini` and the two Ezorsia data files in the game folder.
5. Edit `config.ini`: `ServerIP_Address=127.0.0.1`, the resolution, `WindowedMode=true`, `speedMovementCap=160`.
6. Start `MapleStory.exe` and log in with any new name and password; the server creates the account. Names need at least 4 characters.

Details and the ultrawide notes are in [Client/README.md](../../Client/README.md).

### 2.6 The bot chat (optional)

Bots answer whispers through Claude Haiku, using a Claude subscription through Claude Code.

1. Run `Login-Bot-Chat.bat` once to sign in.
2. Run `Start-Bot-Chat.bat` and leave the window open while playing.

The bridge (`Settings/Scripts/Bot-Chat-Bridge.py`) listens on `127.0.0.1:8585`. The people who play the bots come from `Settings/Bots/`, which was copied from the WowPlus project. The server sends it each whisper to a bot. Each reply is a fresh Claude Code run with no tools, no memory and no access to anything else on the PC.

## 3. Running it day to day

| I want to | Do this |
|-----------|---------|
| Play | Run `Start-Server.bat`, wait for `Cosmic is now online`, start `Client\MapleStory\MapleStory.exe`. |
| Stop | Log out, close the server window, run `Stop-Database.bat`. |
| Back up the save | Run `Backup-Database.bat`. It writes a dated file to `Backups/`. |
| Rebuild after code changes | Close the server window, run `Build-Server.bat`, start the server again. |
| Talk to bots | Run `Start-Bot-Chat.bat` as well. |

Ports: 8484 for login, 7575 to 7577 for the three channels, 3306 for the database, 8585 for the bot chat. All on this PC only.

## 4. Who decides what: server or client

Found by testing. This decides where a change has to be made.

| Thing | Decided by | So you change |
|-------|------------|---------------|
| Buff duration, cooldown, MP and HP cost, buff strength, movement speed | Server | Server skill data only. Works without touching the client. |
| Damage, number of hits, number of targets, hit box | Client | Both copies: the client's so it happens, the server's so they agree and bots match. |
| Tooltip text | Client (`String.wz`) | The client patcher rewrites it. |
| Which monsters a spell or ranged attack hits | Client program | Cannot be changed through data. Melee and area skills follow the target count in the data; skills that fire a projectile or throwing star always hit one. Extra targets for those are added by the server (`plus/SkillSplash.java`). |
| Critical hits | Client, when it holds the Sharp Eyes effect | The server sends that effect to every class (`plus/ClassCrit.java`). |
| Speed cap, damage cap, resolution | Client | `Client/MapleStory/config.ini`. |
| Drops, shops, characters, accounts | Database | SQL. |
| NPC talk, travel prices | Server scripts | `Server/scripts/npc/`. |
| Names a character may not have | Both | The server's list is removed; the client still has its own, which we left alone. |

Other things worth knowing:

- Only the strongest buff of one kind counts. Sprint is the exception we coded: it adds to the running speed buff.
- The server does not limit the damage the client reports. It only compares it with an estimate to flag cheating, and that flagging is off (`USE_AUTOBAN: false`).
- The client lets a character use a skill of another job if the server says the character has it, but does not list it in the skill window. That is how bandits have Flash Jump: the server grants it and puts it on a key.

## 5. How to change things

### 5.1 A setting (rates, switches)

1. Edit `Settings/config.yaml`. The common ones are listed in [Settings/README.md](../README.md).
2. Restart the server.

### 5.2 A skill's numbers

All skill number changes live in one list: `Settings/Scripts/Skill-Changes.tsv`. Never edit the skill data by hand; add a row.

1. Find the skill's ID in `Settings/Reference/Skills.tsv` and its current values per level in `SkillDetails.tsv`.
2. Add a row: skill ID, name, field, value, reason. One row sets one field at every level. The value is a small formula:

   | Letter | Meaning |
   |--------|---------|
   | `L` | The skill level |
   | `M` | The skill's max level |
   | `V` | The value the field has now |
   | `O` | The original value, before our changes |
   | `OM` | The original value at max level |

   Examples: `20`, `90*L`, `max(V, 1800*L//M)`, `round(O*250/OM)`. A hit box corner is written as `x,y` in the fields `lt` (left top) and `rb` (right bottom).

   Common fields: `time` (seconds), `cooltime`, `mpCon`, `hpCon`, `damage`, `attackCount`, `mobCount`, `speed`, `prop` (chance), `x`, `y`, `pdd`, `mdd`.
3. See what would change, then apply to the server data:
   ```
   python Settings/Scripts/Apply-Skill-Changes.py --check
   python Settings/Scripts/Apply-Skill-Changes.py
   ```
4. Close the game, then bring the client's copy and tooltips in line:
   ```
   powershell -ExecutionPolicy Bypass -File Settings\Scripts\Patch-Client-Skills.ps1
   ```
   Add `-CheckOnly` to see the counts without writing anything. The patcher always starts from the untouched originals (`Skill.wz.original`, `String.wz.original` in the game folder), writes to a temporary file, reads it back and only then installs it. To undo everything on the client, copy the `.original` files back.
5. Restart the server (skill data is read at start), start the game, test.
6. Record the change in [Class changes](Class-Changes.md).

Step 4 can be skipped when the change is only a duration, cooldown, cost or buff strength; the game then works correctly but the tooltip shows the old number.

To see what a change does to the balance between classes, run `python Settings/Reference/Build-Reference.py` and then `python Settings/Scripts/Simulate-Damage.py`. It lists every class's damage per use and per second at levels 30, 50, 70 and 100; `--rules` checks that a new job's attack beats the old one from its first point.

Two rules every attack skill follows (Round 4 in the list): level 1 is at least 60% of max, and a new job's main attack starts at least 10% above the old job's max.

### 5.3 A skill's behaviour (not just numbers)

Rules that the data cannot express are in our own package, `Server/src/main/java/plus/`:

| File | What it does |
|------|--------------|
| `ClassCrit.java` | Critical hits for every class, with chance and damage per job tier. |
| `ClassSkills.java` | Paired warrior weapon skills level together; bandits get Flash Jump from 3rd job. |
| `SkillSplash.java` | Extra targets for Energy Bolt, Poison Breath, Holy Arrow, Arrow Blow and Drain. To add a skill, add it to the `SKILLS` set and give it a `mobCount` in `Skill-Changes.tsv`. |

These are called from a few places in the original code, each marked with a `MapleStoryPlus` comment. Search the code for that word to find every hook.

After a code change: close the server, run `Build-Server.bat`, start the server. Then add a row to the "Changes to the server code" table in the Development log.

### 5.4 An NPC, travel price or script

1. Find the NPC's ID in `Settings/Reference/Npcs.tsv`.
2. Edit `Server/scripts/npc/<id>.js`. No restart is needed; the script is read on the next click.

Example already done: the tower teleport stones (`2012014.js`, `2012015.js`, `2040024.js` to `2040027.js`) charge `teleportCost` mesos instead of a scroll.

### 5.5 Drops, shops, characters (database)

Run SQL against the `cosmic` database:

```
Tools\mysql\bin\mysql --defaults-file=Settings\mysql.ini cosmic
```

- Run `Backup-Database.bat` first.
- A character's data is only safe to edit while its account is logged out (`accounts.loggedin = 0`). The server writes the character back on logout and overwrites the edit otherwise.
- Drops are in `drop_data`, shops in `shops` and `shopitems`. The reference lists `Drops.tsv` and `Shops.tsv` show the current content with names.

### 5.5b Where equipment drops, and the drop site

Equipment drops follow rules that a script applies, so that the whole table can be tuned and applied again:

```
python Settings/Scripts/Rebalance-Drops.py --check
python Settings/Scripts/Rebalance-Drops.py
python Settings/Reference/Build-Reference.py
python Settings/Scripts/Make-Drop-Site.py
```

Stop the game server before the second line; it saves a database backup first. Running it twice changes nothing the second time. It only touches equipment dropped by ordinary monsters; bosses, event monsters, scrolls, ores and quest items are left alone.

The rules are described at the top of `Rebalance-Drops.py` and their numbers are just below:

- **Which monsters drop an item:** none more than 5 levels above the level it needs or 20 below; at least 3 between 10 under and 2 over; the plain gear of every class (`Loadouts.tsv`) always has droppers; gear needing level 95 or more also drops from everything above it.
- **Something for every class:** every monster that lives in numbers drops at least one weapon and two armour pieces per class.
- **How often, as a budget:** each monster's total chance is set so that a level of training gives about 8 pieces of gear at a popular hunting spot and 5.5 elsewhere (`PIECES_PER_LEVEL`, `PIECES_ELSEWHERE`), never more than 1 kill in 8. The classes share it equally, and the first gear before level 10 counts five times.

The chances are worked out for the drop and exp rates in `config.yaml`. **After changing those rates, run the script again**, or the amount of gear changes with them.

To see what a rate feels like, run the drop simulation. It changes nothing:

```
python Settings/Scripts/Simulate-Drops.py
python Settings/Scripts/Simulate-Drops.py --class thief
python Settings/Scripts/Simulate-Drops.py --class warrior --levels --to 13
python Settings/Scripts/Simulate-Drops.py --budget 8
```

It shows, per ten levels, how many kills the levels take, how much gear drops, how many kills that is per drop, and how much of it your class would actually wear, with the class weapons counted separately. `--budget N` is a what-if: every level gives about N pieces of gear, whatever the level.

The popular hunting spots are a hand-written list, `Settings/Reference/Hunting-Spots.tsv`: the monster, the levels people train on it, and where. Monsters on it are chosen first when an item needs another dropper, and the bots suggest them when asked where to train.

The drop site is `docs/drops.html`, with its data in `docs/drops-data.js`. Both are written by `Make-Drop-Site.py` from the reference lists, so always rebuild the reference lists first. The page's look is the template at the bottom of that script. To see it, double-click `docs/drops.html`.

In the game every player can type `@whodrops <item>` and `@whatdropsfrom <monster>`.

### 5.6 Monsters, maps, items (server game data)

1. Edit the XML under `Server/wz/`.
2. Restart the server.
3. Rebuild the reference lists so they match: `python Settings/Reference/Build-Reference.py`.
4. If the client needs to show the change, its `.wz` copy needs the same edit. Only skills have a patcher so far.

### 5.7 Client settings

Edit `Client/MapleStory/config.ini`: resolution, windowed or fullscreen, damage cap, speed cap, server address. Keep Windows line endings and do not lengthen the comment lines; the game fails to start otherwise. The resolution must be one the monitor offers.

### 5.8 The bot chat

Two files do the work:

- `Settings/Scripts/bot_minds.py` knows who the bots are: the people, their backgrounds, their typing habits, and how Claude is asked. It is shared with the WowPlus project and must stay identical in both; do not change it for MapleStory alone.
- `Settings/Scripts/Bot-Chat-Bridge.py` is the MapleStory part: what drops where, where monsters live, where to train at a level, the quickest way between maps, and the rules for how a whisper is answered.

The people themselves are in `Settings/Bots/` (see its [README](../Bots/README.md) and the [character sheet](../Bots/Character-Sheet.md)). A bot gets a person the first time it is whispered and keeps them; that pairing is in `Database/BotChat/Assignments.json`.

One name can always be whispered: `GMNova`, the server's GM. It knows what is different on this server (it is told the whole features page, `docs/changes.js`) and it is the only one that remembers you, in `Database/BotChat/maplestory/<your character>/GMNova.json`. Ordinary bots forget a conversation after ten quiet minutes. The details are in the Bots README under "The GM".

| I want to | Do this |
|-----------|---------|
| Change how one person talks | Edit their file in `Settings/Bots/Backgrounds/`, above all the sample lines. |
| Change who a person is | Edit their line in `People.json`, restart the bridge. |
| Change how MapleStory chat sounds | Edit `Settings/Bots/Styles/maplestory.md`. Works at once. |
| Make bots chattier or quieter | The chances at the top of the bridge (`QUESTION_CHANCE`, `JOKE_CHANCE`, `PERSONAL_CHANCE`). |
| Stop bots typing a phrase | The "player, not a guide" rule in the bridge's `system_prompt`. |
| Give a bot a particular person | Put the person's `id` under `maplestory` in `Database/BotChat/Assignments.json`. |
| Change or wipe what the GM remembers about you | Edit or delete `Database/BotChat/maplestory/<your character>/GMNova.json`. |
| Change what the GM knows about the server | Edit `docs/changes.js`; it is read for every answer. |
| Rename the GM | `GM_NAME` in `Server/src/main/java/soloMapling/BotChat/BotChatBridge.java`, then rebuild. |
| Talk to the GM without the game | `python Settings/Scripts/Bot-Chat-Bridge.py --gm --say "how much is a chaos scroll"` (add `--remember` to have the notes written). |
| Write more people in full | `python Settings/Scripts/Make-Bot-Backgrounds.py --count 20` |

After any such change, listen before playing:

```
python Settings/Scripts/Test-Bot-Voices.py
python Settings/Scripts/Bot-Chat-Bridge.py --say "hey" --say "where do i find steelies" --say "gtg"
```

The first puts the same eight lines to six people side by side. Read down each column: could you tell who said what with the names covered, is anyone giving advice nobody asked for, are the lengths uneven. The full list of what to listen for is in the character sheet.

Game knowledge comes from the reference lists: `Drops.tsv`, `Mobs.tsv`, `MobSpawns.tsv`, `TravelLinks.tsv`, `MapLinks.tsv` and `Places.tsv`.

### 5.8b Job advancement and the trials

Explorers advance by level and by beating bosses, through the Guide that the Trade button opens.

| I want to | Do this |
|-----------|---------|
| Change which bosses count for a job | Edit `Settings/Trials.tsv` (band 1 is for 2nd job, 2 for 3rd, 3 for 4th), restart the server. |
| Change how many must be beaten, or the levels | `BANDS` at the top of `Server/src/main/java/plus/Trials.java`, then rebuild. |
| Change what the Guide says | The texts are built in `plus/Trials.java` (`menu`, `jobPage`, `trialsPage`); `Server/scripts/npc/plusGuide.js` only shows them. |
| Change which 4th job skills are free | `FOURTH_JOB_BASICS` in `plus/Trials.java`. |
| See or change what a character has beaten | Table `plus_trials`: one row per character and boss, with the number of kills and the date of the first. Delete a row to undo a trial. |
| Give a test character a trial | `INSERT INTO plus_trials VALUES (<character id>, <mob id>, 1, NOW())` |
| Change how often area bosses come back | `15 * 60 * 1000` in `Server/scripts/event/AreaBoss*.js` (read at server start). |
| Change how long a boss fight takes | `SECONDS`, `SECONDS_HARDEST`, `SECONDS_BAND_1` in `Settings/Scripts/Tune-Bosses.py`, then run it (`--check` first) and restart. It asks the damage simulator what a player does per second at the boss's level. Run it again after changing skills. |
| Change how many tokens a boss gives | The last column of `Settings/Trials.tsv`. Band 4 rows give tokens only. |
| Change what 4th job skills cost | `SKILL_STEP_COST` and `FIRST_KILL_TIMES` in `plus/Trials.java`. |
| Give a test character tokens | `INSERT INTO plus_tokens VALUES (<character id>, 500) ON DUPLICATE KEY UPDATE tokens = 500` |
| Make a 4th job test character | `python Settings/Scripts/Make-Character.py DevHero hero 130 --max-skills` (levels up to 200). |

In the game: the Trade button, any job instructor, or `@goals`.

### 5.9 Prices and the economy

Price and meso changes in the database are made through `Settings/Scripts/Apply-Economy-Changes.py`, not by hand, so they can be repeated on a fresh database. Each change is a small function in that script and is applied once; the table `plus_changes` remembers which ones are in. Stop the game server first. It saves a backup before changing anything. Afterwards run `python Settings/Reference/Build-Reference.py` so the reference lists match.

```
python Settings/Scripts/Apply-Economy-Changes.py --check
python Settings/Scripts/Apply-Economy-Changes.py
```

NX comes from the two NX cards that any monster can drop (table `drop_data_global`; the chances are a change in `Apply-Economy-Changes.py`). Bosses roll them ten times as often, which is one line in `MapleMap.java` marked `MapleStoryPlus`. The drop rate does not apply to these.

Before changing a price, a meso drop or a rate, run the economy estimate. It needs the database running and changes nothing.

```
python Settings/Scripts/Simulate-Economy.py
python Settings/Scripts/Simulate-Economy.py --levels --to 31
python Settings/Scripts/Simulate-Economy.py --potion-price 0.5 --early-meso 2
```

It shows, per ten levels (or per level), how many monsters a player kills, the mesos they drop, what the dropped items sell for at a vendor, and what a warrior, a mage and a thief spend on potions and shop gear. What is real data and what is assumed is described at the top of the script; the assumptions are a block of numbers there.

### 5.10 The set shops in the Free Market

Free Market rooms 1 and 2 have set shops that always sell scrolls and supplies. What they sell and for how much is `Settings/Fixed-Shops.tsv`, which the server reads when it fills the Free Market at start. That file is written by a script; the prices and the layout are tables at the top of the script.

1. Edit the tables in `Settings/Scripts/Make-Fixed-Shops.py` (`SCROLL_PRICE`, the shop lists, `OTHER_SHOPS`).
2. Run `python Settings/Scripts/Make-Fixed-Shops.py`. It says how many shops each room got.
3. Restart the server. The log says `Fixed shops: opened 23 of 23 in Free Market room 1`.

Limits: a shop holds 16 items and a room has 23 shop spots, which is why the scrolls are spread over two rooms. A room not named in the file keeps its random shops.

What vendors pay for equipment (a quarter of the item's data price) is one line in `Server/src/main/java/server/Shop.java`, marked `MapleStoryPlus`.

## 6. Test accounts and characters

Accounts and their characters are listed in [Test-Accounts.md](Test-Accounts.md).

`Make-Character.py` sets up a character in one go: level, job, stats, skills, normal-progression gear, potions and ammo.

```
python Settings/Scripts/Make-Character.py DevBandit bandit 75 --create --max-skills
python Settings/Scripts/Make-Character.py DevPage paladin 35 --no-skills --sp 100
python Settings/Scripts/Make-Character.py trialguy fp 50 --dry-run
```

- Log the account out first.
- `--create` copies the template character `trialguy` on the same account.
- `--max-skills` gives every skill of the jobs reached; `--no-skills --sp N` leaves points to spend by hand.
- Levels 1 to 119. Fourth job is not supported yet.
- It saves a database backup before every real change.

All options and class lines are in [Settings/Scripts/README.md](../Scripts/README.md).

Useful when testing: the GM commands in `Settings/Reference/Commands.tsv`.

## 7. Saving your work

| What | How |
|------|-----|
| Code, settings, docs, server game data | Git: commit and `git push` to `origin`. |
| Database | `Backup-Database.bat`. Local only; never in git. |
| Client changes | Not in git. They can be rebuilt: run the client patcher and re-apply `config.ini`. |

Commit after each working step, with a message that says what changed.

### The features page

`docs/index.html` is a web page listing everything this server has that the original game does not, written for a player. Its content is `docs/changes.js`; `index.html` is a template shared with the WowPlus project and is not edited here.

Whenever something a player would notice is added, changed or removed, update `docs/changes.js` in the same commit and change `updated` at the top. The page shows what the game has right now:

- No ideas or plans; an entry is added when the thing exists.
- No entries for bugs of our own that were fixed.
- When something changes again or is removed, rewrite or delete its entry. Never two entries for one thing.
- Titles say what the player gets ("Any monster can drop something rare"), sentences are short, and the details carry the real numbers from the settings and data, not guesses.
- No file, table or setting names.

To look at it, double-click `docs/index.html`. A missing comma or quote in `changes.js` makes the page come up empty.

## 8. Pitfalls we already hit

| Problem | Cause and fix |
|---------|---------------|
| The game fails at start with `error code : -2147467259` | The resolution in `config.ini` is not one the monitor offers, or the file lost its Windows line endings. |
| A new account cannot be made | The client wants at least 4 characters in the name. |
| "You cannot use this name" for a character | The client's own forbidden-name list. Not changed. |
| A database edit to a character disappears | The account was logged in. Log out first. |
| Choosing a new test character drops the connection | The server remembered the account's characters from before the character was created. Fixed in `Server.java`; before the fix a server restart was needed. |
| A skill change shows in the stat window but not in the tooltip | The tooltip is client text. Run the client patcher. |
| A skill change does nothing | Check section 4: it may be a value the client decides, and the client's copy was not patched. |
| A single-target spell will not hit more monsters | The client program decides that. Use `SkillSplash`. |
| Build fails with files in use | The server is still running. Close it first. |
| `mvnw.cmd` does not run from Git Bash | Run it from PowerShell or the `.bat` file. |
| Sprint did nothing with Haste on | Only the strongest buff of a kind counts. Sprint now adds to the running one. |
| Bots answering with private details | The bot runs must have no tools, no memory and a neutral working folder. This is set in the bridge; keep it that way. |

## 9. Where things are written down

| Question | Document |
|----------|----------|
| What is built but not yet tried in the game | [To test](To-Test.md) |
| What is planned, in what order | [Implementation list](Implementation-List.md) |
| What differs from the original game | [Game changes](Game-Changes.md) |
| Class and skill design, and what is built | [Class changes](Class-Changes.md) |
| What was done and decided; every change to the original code | [Development log](Development-Log.md) |
| Progression design | [Progression design](Progression-Design.md) |
| Ideas not yet planned | [Ideas](Ideas.md) |
| IDs and numbers for everything in the game | [Reference lists](../Reference/README.md) |
| Script options | [Scripts](../Scripts/README.md) |
