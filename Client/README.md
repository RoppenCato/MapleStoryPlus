# Client

The game is installed in `MapleStory/` and works. Downloaded files are in `Downloads/`.

## Plan

Original v83 game install + **MapleEzorsia v2** (`dinput8.dll`) on top.

| Piece | Source | Notes |
|-------|--------|-------|
| v83 installer | [P0nk/Cosmic-client](https://github.com/P0nk/Cosmic-client) (`MapleGlobal-v83-setup.exe`) | The original game. |
| Game data (WZ) | Same repo, `cosmic-wz` | Replaces the installer's WZ files so client and server data match. |
| HD + localhost | [MapleEzorsia v2 releases](https://github.com/444Ro666/MapleEzorsia-v2/releases) (`dinput8.dll`, Release 2, 2023-11-22) | Drop into the game folder. Makes the stock client connect to our server and run in HD. |

Only download Ezorsia from the author's own releases page. Antivirus will likely flag the client files.

## Settings we get (Ezorsia `config.ini`, in the game folder)

| Setting | Default | What it does |
|---------|---------|--------------|
| `width`, `height` | 1280 x 720 | Game resolution. Any value is accepted; the author lists up to 1920x1080. |
| `ServerIP_Address` | 127.0.0.1 | Which server to connect to. Change when friends join. |
| `setDamageCap` | 199999.0 | Damage cap, also for the stats window. Raise it to remove the cap. |
| `speedMovementCap` | 140 | Movement speed cap. |
| `useTubi` | false | Removes the delay after picking up or using items. |
| `WindowedMode` | true | Window or fullscreen. |
| `RemoveLogos` | true | Skips the start-up logos. |
| `MsgAmount` | 26 | Number of exp/pickup messages shown. |
| `useV62_ExpTable` | false | Leave off. |

Do not lengthen the comment lines in `config.ini`; the game crashes if it cannot parse the file.

## Ultrawide (3440x1440)

Solved without extra tools: set an ultrawide resolution in `config.ini` and press Alt+Enter for fullscreen. The display scales it to fill the screen.

**The resolution must be one the monitor and graphics card offer.** Anything else makes the game fail at start with `error code : -2147467259`. 1720x720 failed this way; 1680x720 works.

Ultrawide sizes this PC offers:

| Game resolution | Zoom | Tested |
|-----------------|------|--------|
| 1680x720 | 2x | Works. Current setting, starts in fullscreen (`WindowedMode=false`). |
| 1920x820 | about 1.75x | Not tried |
| 2310x990 | about 1.45x | Not tried |
| 2560x1080 | 1.33x | Not tried |
| 3440x1440 | 1x | Works. Sharpest, small characters, empty space around small maps. |

The game has no zoom of its own. Lower resolution means more zoomed in.

Magpie (in `Tools/Magpie`) gave the same picture as Alt+Enter but made the character stutter, so we do not use it.

When editing `config.ini`, keep Windows line endings. The original is saved as `config.ini.default`.

## Damage cap

- Client: `setDamageCap` in `config.ini`.
- Server: no fixed 199,999 limit found in the code. It calculates an expected maximum per hit for cheat detection, and `USE_AUTOBAN` is off. To be confirmed in play.

## Looked at and not chosen

| Option | Why not |
|--------|---------|
| [izarooni/MapleEzorsia](https://github.com/izarooni/MapleEzorsia) | The original. Resolution only, needs a separate localhost client. v2 replaces it. |
| [BeiDouMS/BeiDou-ijl15](https://github.com/BeiDouMS/BeiDou-ijl15) | Active fork (2026) of Ezorsia v2's first release, made for a Chinese server. Fallback if v2 crashes at the login screen, which it does on some PCs. |
| [OpenStory](https://github.com/rdiol12/OpenStory) | A client rewritten from scratch with UI scaling. Not complete (no mention of party, trade, cash shop, merchants) and no ready-made download. |
| `HeavenMS-localhost-WINDOW.exe` (Cosmic-client) | The standard Cosmic client: 800x600, no settings. Not needed with Ezorsia v2. |

## To check when we install

- Whether the server's `Server/wz/` data matches `cosmic-wz`, or SoloMapling needs its own client WZ edits (its casino code mentions WZ patching).
- The Reddit release post (r/mapleservers, "v83 HD client/localhost release") could not be read from here.
