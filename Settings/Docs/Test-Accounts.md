# Test accounts

Local test logins for our own server. These are not real passwords; do not reuse them anywhere.

| Account | Password | Purpose | Notes |
|---------|----------|---------|-------|
| `devacc` | `devacc` | Test characters, one per class | 15 character slots. Created 2026-10-10 directly in the database. |

## Rules the game client enforces

- Account name: at least 4 characters.
- Character name: 3-12 letters or digits, and not containing a word from the client's forbidden list (`test`, `gm`, `master`, `maple`, town and world names, and more).

## Test characters

All on the `devacc` account, all GM level 6. Rebuilt on 2026-10-10 with every skill of their jobs at max level, so any skill can be tested without spending points. They are test characters, not fair ones: a real character could not have all of these maxed.

| Character | Class | Level | For testing |
|-----------|-------|-------|-------------|
| `trialguy` | Fire/Poison Mage | 75 | Energy Bolt and Poison Breath on groups, Teleport, Element Amplification |
| `DevCleric` | Priest | 75 | Holy Arrow on 3, Bless, Holy Symbol alone, Doom |
| `DevHero` | Crusader | 75 | Crit, Iron Body, Rage, Slash Blast and Coma without HP cost |
| `DevPage` | Page | 35 | Weapon pairs: it has no class skills and 100 unspent skill points. Put a point in Sword Mastery and check Blunt Weapon Mastery follows. |
| `DevBandit` | Chief Bandit | 75 | Savage Blow, Steal, Band of Thieves, Disorder, Assaulter, and Flash Jump being granted on login |
| `DevHermit` | Hermit | 80 | Drain on 3 with one heal, Avenger, Shadow Partner |
| `DevHunter` | Ranger | 75 | Arrow Blow on 3, Focus and Thrust speed, Soul Arrow, Puppet |
| `DevBrawler` | Marauder | 75 | Corkscrew and Backspin on 6, Energy Blast, Dash |
| `DevGunner` | Outlaw | 75 | Double Shot, Invisible Shot, Blank Shot, Grenade, Octopus |

Sprint is on Shift for all of them, except where Shift was already taken (`trialguy`, where it is on Ctrl). Other skills are dragged from the skill window to a key.

To rebuild one, or make another:

```
python Settings/Scripts/Make-Character.py DevHero hero 75 --max-skills
python Settings/Scripts/Make-Character.py DevPage paladin 35 --create --no-skills --sp 100
```

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
