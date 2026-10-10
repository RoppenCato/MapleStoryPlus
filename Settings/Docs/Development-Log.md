# Development log

What we have done, decided and changed. Newest first.

## 2026-10-10: Project set up

**Done**

- Cloned [SoloMapling](https://github.com/MadaraGameDev/SoloMapling) (commit `47b61b538`, branch `main`) into `Server/`.
- Original repo linked as `upstream`, pushing disabled.
- Folder layout: `Server/`, `Client/`, `Settings/`.
- `Settings/config.yaml` is our live settings file, copied from the original.
- `Start-Server.bat` starts the server with our settings file.

**Decided**

- Work locally first. A private GitHub repo for backup comes later.
- The game client, its data files, the database and its backups stay out of GitHub. The server's own data (`Server/wz/`, part of the original repo) is included, since we will be editing it.

- Java 21 and MySQL installed directly, not Docker.
- Both are unpacked into `Tools/` instead of installed on Windows, because this PC has no winget and installers need admin rights. Nothing was added to the system PATH or to Windows services.
- Database user is `root` with an empty password, reachable only from this PC. Set a real password before friends connect.

**Server running**

- Amazon Corretto 21.0.12 in `Tools/java21`, MySQL 8.4.11 in `Tools/mysql`, data in `Database/`.
- MySQL settings in `Settings/mysql.ini`.
- Created the empty `cosmic` database; the server filled it on first start (75 tables).
- Built with `mvnw.cmd clean package -Dmaven.test.skip` (tests skipped).
- Started with `Start-Server.bat`: online, all bot waves ran.

**Client**

- Chosen: original v83 install + MapleEzorsia v2 (see `Client/README.md`).
- Downloaded to `Client/Downloads`: v83 installer and Cosmic game data (P0nk/Cosmic-client), Ezorsia v2 Release 2.

**Backups**

- The project folder is now one git repo (branch `main`). The original server is merged in under `Server/` with its history; the separate git folder inside `Server/` is gone.
- Remotes: `origin` = our GitHub repo, `upstream` = SoloMapling (push disabled).
- `Backup-Database.bat` saves the database to `Backups/` (local only).

**Planning**

- Added the Implementation list, Game changes and Class changes documents.

**Open**

- Install the client and log in.
- Test companion bots in game (do they take damage, follow into boss rooms, count for party quests).

**Decided later the same day**

- Solo by default, with companion bots as optional extra damage.
- The GitHub repo (`RoppenCato/MapleStoryPlus`) is public. Nothing private goes in it.

## 2026-10-10: Reference lists and character tool

- `Settings/Reference/`: lists of jobs, skills, maps, monsters, NPCs, items, drops, shops, scrolls, skill details, quests and GM commands, plus a hand-written travel list.
- `Settings/Scripts/Make-Character.py`: sets up a test character (level, job, stats, skills, gear, supplies). Tested in check mode only.
- `trialguy` was set by hand to a level 50 Fire/Poison Wizard before the tool existed. It still wears the level 50 Zhu-Ge-Liang Wand, which is not a normal-progression weapon.
- Found: the tower travel scrolls (Orbis Rock Scroll, Eos Rock Scroll) are not sold in any shop and not in the drop table.

## 2026-10-10: First game changes (Round 1 tests)

Results from Robin's tests, 2026-10-10:

- Sprint works from the server's skill data alone: speed, duration, cooldown and MP cost all took effect with no client edit.
- Haste lasts 30 minutes from the server's skill data alone. The tooltip still shows the old duration, since that text is in the client's data.
- Flash Jump works on a Chief Bandit: the client does not refuse another job's skill. It does not appear in the bandit's skill window, only as a key binding, so the server will have to grant it and offer a way to bind it.
- Buffs of the same kind do not add up. With Haste on, sprint did nothing, because only the strongest speed buff counts. Fixed in server code afterwards (see the code change list); that fix is not tested yet.
- One client freeze happened when sprint was used right after Flash Jump. It did not happen again in later tries on either the bandit or a real Hermit. Cause unknown; possibly coincidence.
- Still open: whether the raised speed cap (160) works. The stat window showed 140 with Haste, which the stacking problem explains.

- `Settings/Scripts/Apply-Skill-Changes.py` applies the rows in `Skill-Changes.tsv` to the server's skill data. Running it twice changes nothing the second time.
- Applied to `Server/wz/Skill.wz`: Haste lasts 30 minutes at max (bandit and assassin); Nimble Feet is the sprint (+10 speed, 10 seconds, 20-second cooldown, no MP cost).
- Client: `speedMovementCap=150` in `Client/MapleStory/config.ini` (was 140). The client folder is not in git.
- Test character `DevBandit` (level 70 Chief Bandit) created with the character tool, its first real run with `--create`, and given the Hermit's Flash Jump directly in the database.

What the tests answer: whether buff durations and speed are decided by the server alone, and whether the client lets a job use another job's skill.

## Changes to the server code

Every change we make to the original code, so we know what to check when pulling updates from `upstream`.

| Date | File | Change | Why |
|------|------|--------|-----|
| 2026-10-10 | `Server/src/main/java/config/YamlConfig.java` | Config file path can be set with `-Dconfig-path=...`; default is still `config.yaml`. | So the server reads `Settings/config.yaml`. |
| 2026-10-10 | `Server/src/main/java/client/Character.java` | Removed the blocked-word list for character names (`BLOCKED_NAMES`). Names must still be unused and 3-12 letters or digits. | It blocked ordinary names such as "Test". |
| 2026-10-10 | `Server/src/main/java/net/server/channel/handlers/WhisperHandler.java` | A whisper to a bot is also passed to the bot chat bridge. | Bots answer whispers through Claude Haiku (prototype). |
| 2026-10-10 | `Server/src/main/java/soloMapling/BotChat/BotChatBridge.java` (new) | Sends the whisper to the bridge on `127.0.0.1:8585` and whispers the reply lines back. Silent if the bridge is not running. | Same. |
| 2026-10-10 | `Server/scripts/npc/2012014.js`, `2012015.js`, `2040024.js` to `2040027.js` | The tower teleport stones charge `teleportCost` (5,000 mesos) instead of using up a rock scroll. | `T-2`. The scrolls could not be obtained. |
| 2026-10-10 | `Server/src/main/java/server/StatEffect.java`, `Server/src/main/java/client/Character.java` | Sprint (Nimble Feet) adds its speed to the speed buff already running, in the packet to the client and in the server's own record. | The server only counts the strongest buff of a kind, so a +20 sprint lost to Haste's +40. Not tested in game yet. |
