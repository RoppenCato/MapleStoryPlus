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

### 5.6 Monsters, maps, items (server game data)

1. Edit the XML under `Server/wz/`.
2. Restart the server.
3. Rebuild the reference lists so they match: `python Settings/Reference/Build-Reference.py`.
4. If the client needs to show the change, its `.wz` copy needs the same edit. Only skills have a patcher so far.

### 5.7 Client settings

Edit `Client/MapleStory/config.ini`: resolution, windowed or fullscreen, damage cap, speed cap, server address. Keep Windows line endings and do not lengthen the comment lines; the game fails to start otherwise. The resolution must be one the monitor offers.

### 5.8 The bot chat

The code is in `Settings/Scripts/Bot-Chat-Bridge.py`: what the bots know (drops, where monsters live, routes), the rules they follow, and the filter on what they may say.

Who the bots are is in `Settings/Bots/` (see its [README](../Bots/README.md)): 300 made-up people in `People.json`, the lists they are built from in `Traits.json`, and how MapleStory chat sounds in `Styles/maplestory.md`. A bot gets a person the first time it is whispered and keeps that person; the pairing is saved in `Database/BotChat/Assignments.json`. Conversations themselves are not saved.

| I want to | Do this |
|-----------|---------|
| Change one person | Edit their line in `People.json`, restart the bridge. |
| Add more people or new traits | Edit `Traits.json`, run `python Settings/Scripts/Make-Bot-People.py`. |
| Change how chat sounds | Edit `Styles/maplestory.md`. Works at once. |
| Give a bot a particular person | Put the person's `id` under `maplestory` in `Database/BotChat/Assignments.json`. |

Test without the game:

```
python Settings/Scripts/Bot-Chat-Bridge.py --say "where do I find slimes?"
```

Travel knowledge comes from `Settings/Reference/TravelLinks.tsv`, `MapLinks.tsv` and `Places.tsv`.

### 5.9 Prices and the economy

Before changing a price, a meso drop or a rate, run the economy estimate. It needs the database running and changes nothing.

```
python Settings/Scripts/Simulate-Economy.py
python Settings/Scripts/Simulate-Economy.py --levels --to 31
python Settings/Scripts/Simulate-Economy.py --potion-price 0.5 --early-meso 2
```

It shows, per ten levels (or per level), how many monsters a player kills, the mesos they drop, what the dropped items sell for at a vendor, and what a warrior, a mage and a thief spend on potions and shop gear. What is real data and what is assumed is described at the top of the script; the assumptions are a block of numbers there.

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
| What is planned, in what order | [Implementation list](Implementation-List.md) |
| What differs from the original game | [Game changes](Game-Changes.md) |
| Class and skill design, and what is built | [Class changes](Class-Changes.md) |
| What was done and decided; every change to the original code | [Development log](Development-Log.md) |
| Progression design | [Progression design](Progression-Design.md) |
| Ideas not yet planned | [Ideas](Ideas.md) |
| IDs and numbers for everything in the game | [Reference lists](../Reference/README.md) |
| Script options | [Scripts](../Scripts/README.md) |
