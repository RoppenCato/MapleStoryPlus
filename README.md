# MapleStoryPlus

Our own private MapleStory v83 server. Runs locally for now; playing with friends comes later.

## Folders

| Folder | What it is |
|--------|------------|
| [Server](Server/) | The server code. A copy of [SoloMapling](https://github.com/MadaraGameDev/SoloMapling) (Cosmic v83 emulator + bots that fill the world). |
| [Client](Client/) | The game client we play with. Not chosen yet, see [Client/README.md](Client/README.md). |
| [Settings](Settings/) | Our personal settings (`config.yaml`: rates, worlds, gameplay switches) and our documentation. |
| `Database/` | The MySQL data: accounts, characters, items. This is the save file, so back it up. |
| `Tools/` | Java 21 and MySQL 8.4, unpacked here instead of installed on Windows. Delete the folder to remove them. |

## Where to change things

- **Rates and gameplay settings:** edit [Settings/config.yaml](Settings/config.yaml). The guide is in [Settings/README.md](Settings/README.md).
- **Server code:** edit files under `Server/`, then rebuild.

## Documentation

| Document | What it is |
|----------|------------|
| [Implementation list](Settings/Docs/Implementation-List.md) | The plan: what we do and in what order, ticked off as we go. |
| [Ideas](Settings/Docs/Ideas.md) | Things we might do, grouped by area. Not decided or planned. |
| [Game changes](Settings/Docs/Game-Changes.md) | What is different from the original game. |
| [Class changes](Settings/Docs/Class-Changes.md) | Goals and changes per class and skill. |
| [Reference lists](Settings/Reference/README.md) | Names, IDs and numbers: jobs, skills, maps, monsters, NPCs, items, drops, shops, scrolls, quests, GM commands, travel. |
| [Scripts](Settings/Scripts/README.md) | The tool that sets up a test character with level, skills and gear. |
| [Progression design](Settings/Docs/Progression-Design.md) | The solo progression: trial bands, tokens, job levels and skill points. Design in progress. |
| [Bosses and party quests](Settings/Docs/Bosses-and-Party-Quests.md) | Every boss and party quest the server has: players, levels, HP, where, respawn. Built automatically. |
| [Research: other servers](Settings/Docs/Research-Other-Servers.md) | What popular servers changed about classes and skills, as ideas for ours. |
| [Research: bots and bosses](Settings/Docs/Research-Bots-and-Bosses.md) | How the bots work and what each boss needs. |
| [Development log](Settings/Docs/Development-Log.md) | What we did and decided, and which server files we changed. |

## Starting and stopping

| Script | What it does |
|--------|--------------|
| `Start-Server.bat` | Starts the database if it is not running, then the game server, using `Settings/config.yaml`. |
| `Stop-Database.bat` | Shuts the database down cleanly. Close the game server window first. |
| `Backup-Database.bat` | Saves a copy of the database to `Backups/`. |
| `Start-Bot-Chat.bat` | Prototype: lets bots answer whispers through Claude Haiku. Leave the window open while playing. |
| `Login-Bot-Chat.bat` | One-time Claude login for the bot chat. |
| `Build-Server.bat` | Rebuilds the server after code changes. |

The server is online when the window says `Cosmic is now online`. It listens on port 8484 (login) and 7575-7577 (channels). The database only accepts connections from this PC.

## Status

- [x] Java 21 (Amazon Corretto 21.0.12, in `Tools/java21`)
- [x] MySQL 8.4.11 (in `Tools/mysql`, data in `Database/`)
- [x] Server built and starts
- [ ] Client installed and first login (files are downloaded in `Client/Downloads`)

## Backups

| What | How |
|------|-----|
| Code, settings and docs | Git. The whole `MapleStoryPlus` folder is one repo; our GitHub repo is the remote `origin`. |
| Database (accounts, characters) | Run `Backup-Database.bat`. It saves a dated file in `Backups/`. These stay on this PC and are not sent to GitHub. |

Not in git: `Tools/`, `Database/`, `Backups/`, the game client and its downloads. Tools and client can be downloaded again.

## The original repo

The original server code (SoloMapling) is merged in under `Server/`, with its history. It is linked as the remote `upstream`, with pushing disabled, so nothing here can end up there.

To pull in their updates later:

```
git fetch upstream
git merge -X subtree=Server upstream/main
```

Our own changes to the server code are listed in the Development log, so we know what to check after such a merge.
