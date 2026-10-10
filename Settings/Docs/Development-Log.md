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
- Game data (`wz/`) and passwords stay out of any GitHub repo of ours.

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

**Planning**

- Added the Implementation list, Game changes and Class changes documents.

**Open**

- Install the client and log in.
- Solo or bots in the party: decide after looking at how the bots work (Implementation list, section 1).

## Changes to the server code

Every change we make to the original code, so we know what to check when pulling updates from `upstream`.

| Date | File | Change | Why |
|------|------|--------|-----|
| 2026-10-10 | `Server/src/main/java/config/YamlConfig.java` | Config file path can be set with `-Dconfig-path=...`; default is still `config.yaml`. | So the server reads `Settings/config.yaml`. |
| 2026-10-10 | `Server/src/main/java/client/Character.java` | Removed the blocked-word list for character names (`BLOCKED_NAMES`). Names must still be unused and 3-12 letters or digits. | It blocked ordinary names such as "Test". |
