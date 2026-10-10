# Test accounts

Local test logins for our own server. These are not real passwords; do not reuse them anywhere.

| Account | Password | Purpose | Notes |
|---------|----------|---------|-------|
| `devacc` | `devacc` | Test characters, one per class | 15 character slots. Created 2026-10-10 directly in the database. |

## Rules the game client enforces

- Account name: at least 4 characters.
- Character name: 3-12 letters or digits, and not containing a word from the client's forbidden list (`test`, `gm`, `master`, `maple`, town and world names, and more).

## Test characters

Suggested names: `DevWarrior`, `DevMage`, `DevBowman`, `DevThief`, `DevPirate`.

| Character | Class | Level | GM | Notes |
|-----------|-------|-------|----|-------|
| `trialguy` | Fire/Poison Wizard | 50 | 6 | Set up in the database 2026-10-10 with level 50 gear, skills and 1M meso. |
| `DevBandit` | Chief Bandit | 70 | 6 | Created 2026-10-10 with the character tool for the Round 1 tests. Has the Hermit's Flash Jump as a test. Keys: Q Savage Blow, R Haste, T Dagger Booster, A Flash Jump, Shift sprint (Nimble Feet). |

## GM commands

Typed in the game chat. GM commands start with `!`. `!help` lists them.

| Command | What it does |
|---------|--------------|
| `!goto <place>` | Warp to a town by name, for example `!goto ellinia` |
| `!warp <map id>` | Warp to a map by its number |
| `!level <number>` | Set your level |
| `!job <job id>` | Set your job |
| `!item <item id>` | Give yourself an item |
| `!heal` | Restore HP and MP |
| `!maxstat`, `!maxskill` | Max out stats or skills |
| `!spawn <mob id>`, `!killall` | Spawn a monster, or kill everything on the map |
