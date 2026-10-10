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

## Changes to the server code

Every change we make to the original code, so we know what to check when pulling updates from `upstream`.

| Date | File | Change | Why |
|------|------|--------|-----|
| 2026-10-10 | `Server/src/main/java/config/YamlConfig.java` | Config file path can be set with `-Dconfig-path=...`; default is still `config.yaml`. | So the server reads `Settings/config.yaml`. |
| 2026-10-10 | `Server/src/main/java/client/Character.java` | Removed the blocked-word list for character names (`BLOCKED_NAMES`). Names must still be unused and 3-12 letters or digits. | It blocked ordinary names such as "Test". |
