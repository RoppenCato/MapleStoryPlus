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
- After the stacking fix: Haste plus sprint reaches 160 and drops back to 140 when the sprint ends. The fix and the raised speed cap both work (confirmed by Robin).

**Round 1b, loaded and spot-checked by Robin (buffs last far longer; not timed to the full 30 minutes, and not all 85 skills tried):** every duration and cooldown agreed in the class design, 98 rows in `Skill-Changes.tsv` covering 85 skills. All boosters, class buffs, Maple Warrior and summons last 30 minutes at max; Puppet, Dash and the two Transformations 3 minutes; Infinity, the energized state and the Octopus turrets 2 minutes; Mystic Door 10 minutes; Smokescreen has a 5-minute cooldown; the Cygnus and Aran versions of Nimble Feet match the sprint. Lower skill levels scale up in step and never get shorter than they were.

- `Settings/Scripts/Apply-Skill-Changes.py` applies the rows in `Skill-Changes.tsv` to the server's skill data. Running it twice changes nothing the second time.
- Applied to `Server/wz/Skill.wz`: Haste lasts 30 minutes at max (bandit and assassin); Nimble Feet is the sprint (+10 speed, 10 seconds, 20-second cooldown, no MP cost).
- Client: `speedMovementCap=150` in `Client/MapleStory/config.ini` (was 140). The client folder is not in git.
- Test character `DevBandit` (level 70 Chief Bandit) created with the character tool, its first real run with `--create`, and given the Hermit's Flash Jump directly in the database.

What the tests answer: whether buff durations and speed are decided by the server alone, and whether the client lets a job use another job's skill.

**Round 1c, loaded and confirmed by Robin on the tested skills (Iron Body, Slash Blast, Sword Booster, Rage, Teleport, Dark Sight). Buff strength, HP and MP costs are controlled by the server; no client edit needed:** 53 more rows in `Skill-Changes.tsv` for values the server is believed to control. Stronger Iron Body, Magic Armor and Iron Will, with +20 speed on Iron Body; no HP cost on boosters and everyday attacks; Rage without its defence penalty; Threaten and Disorder at -30; skills that always work at max level (Shout, Seal, Doom, Power Knock-Back, Poison Breath, Poison Mist, Pickpocket); 3-second freezes; cheaper Teleport; ultimates capped at 2,500 MP; Element Amplification without extra MP cost at max; Dark Sight without its speed penalty; Dash at +20. Also `USE_FULL_HOLY_SYMBOL: true` in `Settings/config.yaml`.

**Found while building crit:** the server does not limit the damage a client reports. It only compares it with its own estimate to flag cheating, and that flagging is switched off. So for damage, hit counts and target counts the client's skill data is what decides; the server's copy matters for bots and for keeping the two in step.

**Round 2, tested by Robin: the game starts and plays with the patched skill file, and Double Stab, Savage Blow and Steal behave as changed.** Two follow-ups from that test, installed and confirmed by Robin ("everything works I think"): tooltips are rewritten from the same list (2,626 level texts), and Steal gets a hit box, because without one it only reached monsters standing on the same spot. Details of the first install: the client's skill file is now patched from the same list as the server (`Patch-Client-Skills.ps1`). First client-side changes: Double Stab 160% per hit at max, Savage Blow 6 hits at every level from 55% to 100%, Steal on 4 to 6 monsters. The patch also brings the client's copy in line with the server for every earlier change (3,241 values changed, 91 added). Read-back check passed; whether the game starts and plays with the patched file is the test.

**Round 3, installed but not tested in game:** the rest of the number changes from the class design (55 more rows: damage, target counts and hit boxes), plus the code changes listed at the end of this document. `Apply-Skill-Changes.py` can now scale from a skill's original values (`O` and `OM` in formulas), read from git, so scaled changes stay repeatable. What is built and what is not is tracked at the top of [Class-Changes.md](Class-Changes.md).

## 2026-10-11: Bot chat rebuilt on the shared bot_minds.py

- WowPlus reworked how bots talk (full backgrounds, fixed typing habits, rules found by listening) and copied the result here. `Bot-Chat-Bridge.py` now uses `bot_minds.py` for everything about who a bot is, and keeps only the MapleStory parts. `bot_minds.py` was not changed.
- Game facts are handed to the bot as something it knows, so it says them in its own voice.
- New from this project: training suggestions by level from the monster data, and `Test-Bot-Voices.py` adapted for MapleStory. What listening changed is listed in `Settings/Bots/README.md`.
- Tested outside the game only. The server side is unchanged: it still sends whispers to port 8585.
- Not taken over: memory and bots speaking first. Waiting for Robin's decision.

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
| 2026-10-11 | `Server/src/main/java/plus/ClassCrit.java` | Crit is the same in every job: 40% for 150% (was four tiers). | Robin's decision after the class review. Not tested in game yet. |
| 2026-10-10 | `Server/src/main/java/plus/ClassCrit.java` (new), `server/maps/MapleMap.java`, `client/Character.java`, `net/server/channel/handlers/AbstractDealDamageHandler.java` | Critical hits for every class: each character is sent the Sharp Eyes effect with its job's chance and damage when it enters a map or changes job. Classes with their own crit (bowmen, assassins) and beginners are left out. | Agreed class rule. Tested in game on a Crusader: works. |
| 2026-10-10 | `Server/src/main/java/plus/ClassSkills.java` (new), `client/processor/stat/AssignSPProcessor.java`, `client/Character.java`, `server/maps/MapleMap.java` | Paired warrior weapon skills level together. Chief Bandits and Shadowers are given Flash Jump (level follows character level from 70) and it is put on a free key. | Agreed class changes. Not tested in game yet. |
| 2026-10-10 | `Server/src/main/java/net/server/channel/handlers/AbstractDealDamageHandler.java` | Drain and the other draining attacks heal from one monster per use, based on the damage to that monster. Before, the heal was worked out for every monster hit, from the running total. | Drain now hits up to 3 monsters; the healing must not grow with it. Not tested in game yet. |
| 2026-10-10 | `Server/src/main/java/net/server/Server.java` (`haveCharacterEntry`) | When a chosen character is not in the server's list for the account, the account's characters are read from the database again before the choice is refused. | The list is filled at the account's first login after a server start. Characters made by `Make-Character.py --create` after that were shown at character select but dropped the connection when chosen. Not confirmed in game on one of those characters yet. |
| 2026-10-11 | `Server/src/main/java/plus/FixedShops.java` (new), `soloMapling/FreeMarket/ArtificialFreeMarket.java` (`populateFreeMarketRoom`) | A Free Market room listed in `Settings/Fixed-Shops.tsv` gets the shops from that file instead of random ones. Their stock is refilled after every purchase and nothing about them is saved to the database. | Scrolls and supplies that are always for sale. All 41 shops open at start; buying from one is not tested in game yet. |
| 2026-10-11 | `Server/src/main/java/server/Shop.java` (`sell`) | Equipment sold to a vendor pays a quarter of its data price. | Selling equipment drops flooded the late game with mesos (see `Simulate-Economy.py`). Not tested in game yet. |
| 2026-10-10 | `Server/src/main/java/plus/SkillSplash.java` (new), `net/server/channel/handlers/AbstractDealDamageHandler.java` | Energy Bolt, Poison Breath, Holy Arrow, Arrow Blow and Drain: when one of them damages a monster, the server deals the same damage (give or take 10%, rolled per monster) to the nearest monsters within 200 pixels of it, up to the skill's target count, just after the first hit shows (the hit delay the client reports plus 0.15 s, at least 0.7 s). Poison Breath's poison is rolled for each of them. | The client keeps these skills on one target whatever the skill data says (tested with the target count and hit box, and with Energy Bolt's projectile removed). Tested in game by Robin: works (which of the five skills were tried is not recorded). |
