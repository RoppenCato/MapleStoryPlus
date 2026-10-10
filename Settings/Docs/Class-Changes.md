# Class changes

One section per class: the goal we agreed on, the ideas, and every change made. Belongs to section 9 (`K`) of the [Implementation list](Implementation-List.md).

## How to use

- **Goal:** one or two sentences on how the class should feel. Filled in when we discuss the class.
- **Ideas:** things to consider, not decided.
- **Changes:** one row per change, added when it is implemented and tested.

Status values: `idea`, `planned`, `done`, `dropped`.

Change table columns:

| Date | Skill | Before | After | Why | Status |
|------|-------|--------|-------|-----|--------|

## All classes

**Goal:** not set.

**Ideas**

- Review damage and MP/HP costs of all skills.
- **Agreed 2026-10-10: long buffs for every class.** Weapon boosters, Haste and similar self-buffs last 30 minutes at max level (every booster lasts 200 seconds today). Which buffs count as "similar" is settled class by class.

**Changes:** none yet.

---

## Warriors

Hero, Paladin, Dark Knight.

**Goal:** not set.

**Ideas**

- Something to speed them up (movement).

**Changes:** none yet.

## Magicians

Fire/Poison, Ice/Lightning, Bishop.

**Goal:** not set.

**Ideas**

- Stronger bonus against elemental weaknesses.

**Changes:** none yet.

## Bowmen

Bowmaster, Marksman.

**Goal:** not set.

**Ideas:** none yet.

**Changes:** none yet.

## Thieves

### Bandit line (Rogue, Bandit, Chief Bandit, Shadower)

Under discussion since 2026-10-10. Ideas from other servers are in [Research-Other-Servers.md](Research-Other-Servers.md).

**Goal (set 2026-10-10):** a fast melee thief. Mobility and group attacks are fixed first; the meso skills stay as flavour and should work without chores.

**Plan**

Status: `agreed` = Robin decided it. `proposed` = suggested, not yet confirmed. Nothing is built.

| # | Job | Change | Status | Needs |
|---|-----|--------|--------|-------|
| 1 | Rogue | Double Stab gets an overall damage buff: 160% per hit at max instead of 140% (320% in total, was 280%). | agreed | Server and client skill data |
| 2 | Bandit | Savage Blow is better than a maxed Double Stab from its first point, and stronger overall: 6 hits at every level, 55% per hit at level 1 (330%) growing to 100% at level 30 (600%, was 480%). | agreed | Server and client skill data |
| 3 | Bandit | Steal hits 4 monsters from level 1 and 6 when maxed. | agreed | Server and client skill data |
| 4 | Bandit | Dagger Booster and Haste last 30 minutes (now 200 seconds at max). | agreed | Server and client skill data |
| 5 | Chief Bandit | Flash Jump at 3rd job, the same point where Hermits get it. | agreed | To be tested: the client may refuse another job's skill |
| 6 | Chief Bandit | Assaulter is faster and travels further, so it works as movement. | proposed | Client data, possibly client code |
| 7 | Chief Bandit | Pickpocket drops mesos far more reliably and lasts longer, so Meso Explosion always has something to explode. | proposed | Server data |
| 8 | Chief Bandit | Meso Guard lasts longer (180 seconds, or 30 minutes like the other buffs). | proposed | Server and client skill data |
| 9 | Shadower | Assassinate does full damage without the Dark Sight setup. | proposed | To be tested |
| 10 | All | Dark Sight is a toggle and any attack leaves it. | proposed | Client code, likely hard |
| 11 | Shadower | Boomerang Step works on slopes and at ledges. | proposed | Client code, likely hard |

Why the bandit needs the damage buff: at 2nd job an Assassin's Lucky Seven does 300% from range and Critical Throw adds about half again on average, while a Bandit's Savage Blow does 480% in melee with a slower swing.

Order when we build: Savage Blow first, because it is also the first test of how a skill edit is made at all (`R-4`).

**How it plays now** (numbers from `SkillDetails.tsv`)

| Job | Main tools | What is wrong |
|-----|------------|---------------|
| Rogue (10) | Double Stab: 2 hits, 196% total at level 1, 280% at max | Fine |
| Bandit (30) | Savage Blow: 160% total at level 1, 480% at max. Haste, Steal, Dagger Booster | Savage Blow is worse than a maxed Double Stab until level 9 (288% against 280%). The first 8 points buy nothing. |
| Bandit (30) | Nothing hits more than one monster | No group attack at all until 3rd job, 40 levels later |
| Chief Bandit (70) | Band of Thieves (6 targets, 210% at max), Assaulter (450%, one target, stun), Meso Guard, Meso Explosion, Pickpocket, Chakra | Meso Explosion needs mesos on the ground, which is fiddly alone. Assaulter moves you but is slow. |
| Shadower (120) | Assassinate (3 hits of 600% from Dark Sight), Boomerang Step (2 hits of 500%, up to 4 targets), Shadow Shifter, Smokescreen, Venomous Stab | Assassinate needs Dark Sight first. Everything needs mastery books. |
| All | No Flash Jump. Assassins get it at 3rd job. | Slow to move around compared with the other thief |

**Ideas**

| Idea | Kind | Notes |
|------|------|-------|
| Flash Jump for the bandit line | New skill for the class | Robin's idea. The skill exists for Hermits (Flash Jump, 20 levels). Giving it to another job needs testing: the client may not let a Chief Bandit use a Hermit skill. |
| Savage Blow useful from level 1 | Rescale | Start at 6 hits and grow the damage, or raise the early damage, so the first point already beats Double Stab |
| A group attack in 2nd job | Rescale or new use | Let Savage Blow or Steal hit 2 to 3 monsters, or bring Band of Thieves forward |
| Assaulter as movement | Speed | Faster and longer dash, as players on other servers ask for |
| Dark Sight as a toggle | Quality of life | From MapleRoyals: press again to cancel, any attack leaves it |
| Assassinate without the Dark Sight setup | Simplify | From MapleRoyals: full damage without charging in Dark Sight |
| Steal's attack buff lasts longer | Small buff | From Classic World: 60 seconds instead of 30 |
| Meso Explosion without the chore | Rework | Pickpocket already drops mesos on hit; make the two work together smoothly, or let Meso Explosion drop its own |
| Boomerang Step usable on slopes and ledges | Fix | From MapleRoyals |

**Changes:** none yet.

### Assassin line (Rogue, Assassin, Hermit, Night Lord)

**Goal:** not set.

**Ideas:** none yet.

**Changes:** none yet.

## Pirates

Buccaneer, Corsair.

**Goal:** not set.

**Ideas:** none yet.

**Changes:** none yet.

## Cygnus Knights

Dawn Warrior, Blaze Wizard, Wind Archer, Night Walker, Thunder Breaker.

**Goal:** not set.

**Ideas:** none yet.

**Changes:** none yet.

## Aran

**Goal:** not set.

**Ideas:** none yet.

**Changes:** none yet.

---

## Open questions

- Which classes are playable on our server? The server code has Evan skills; whether Evan works in a v83 client is not checked.
- Do skill changes need matching edits in the client's data? See `R-4`.
