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
- **Agreed 2026-10-10: Maple Warrior lasts 30 minutes** for every 4th job (now 15).
- **Agreed 2026-10-10: critical hits for every class (Robin's idea).** Classes that have their own critical skill keep it: bowmen (Critical Shot) and assassins (Critical Throw). Every other class gets a lesser, built-in version that grows with each job advancement.

  | Job | Chance | A critical hit does |
  |-----|--------|---------------------|
  | 1st | 10% | 150% |
  | 2nd | 15% | 150% |
  | 3rd | 20% | 160% |
  | 4th | 25% | 170% |

  For comparison, a bowman's Critical Shot is 40% for 200%.

  How: the server gives the character the same effect as the bowmaster's Sharp Eyes buff, permanently. The client already shows critical hits for any class under that buff, so nothing in the client changes. Not tested. Doubt: in the original game Sharp Eyes does not affect magic, so magicians may not be able to crit this way.

**Changes:** none yet.

---

## Warriors

Hero, Paladin, Dark Knight. Under discussion since 2026-10-10, one job at a time.

**Goal:** not set. Starting point: the warrior is the sturdiest class and the only one with a group attack in 1st job. Its weaknesses are movement and constant HP and MP costs.

**Decided (Robin, 2026-10-10):** warriors get critical hits. This became the rule for all classes at the top of this document.

### Swordman (shared 1st job)

| # | Change | Status | Needs |
|---|--------|--------|-------|
| 1 | Slash Blast has no HP cost (now 16 HP per swing at max). | agreed | Server and client skill data |
| 2 | Iron Body lasts 30 minutes (now 300 seconds) and gives +80 weapon defence (now +40) and +40 magic defence (now none). | agreed | Server and client skill data |
| 3 | Iron Body also gives +20 movement speed. This is the warrior's speed-up, done the certain way first; a real dash skill is a later idea. | agreed | Server and client skill data |
| 4 | Critical hits: covered by the rule for all classes at the top of this document. Endure is not reworked for it and stays as it is. | agreed | See the rule |
| 5 | Power Strike, Improved HP Recovery and Improved MaxHP Increase stay as they are. | agreed | Nothing |

### Paired weapon skills (rule for all warriors)

Robin, 2026-10-10: Sword Mastery and Axe Mastery should be bundled into one.

How: the two skills level together. A point put into one gives the same point in its twin for free, so a warrior pays for the pair once and can switch weapon type without losing anything. The client still shows two skills, each working for its own weapon; only the server's handling of skill points changes. Not tested.

| Pair | Status |
|------|--------|
| Fighter: Sword Mastery and Axe Mastery | agreed |
| The other 2nd job pairs: Final Attack and Booster for the Fighter; Mastery, Final Attack and Booster for the Page (sword and blunt weapon) and the Spearman (spear and pole arm) | agreed |
| 3rd job pairs, such as Panic and Coma for sword and axe, the element charges for sword and blunt weapon, Crusher and Dragon Fury for spear and pole arm | agreed |

### Fighter (2nd job)

The Fighter gets no new attack in 2nd job; it keeps Power Strike and Slash Blast. Final Attack, a permanent Rage and the crit rule are its gains. If it feels flat in play, the fix is a damage bump to those two 1st job attacks.

| # | Change | Status | Needs |
|---|--------|--------|-------|
| 1 | Sword Mastery and Axe Mastery are bundled, by the pairing rule above. | agreed | Server code |
| 2 | Sword Booster and Axe Booster last 30 minutes (now 200 seconds) and have no HP cost. | agreed | Server and client skill data |
| 3 | Rage lasts 30 minutes (now 160 seconds) and has no defence penalty (now -12 weapon defence). | agreed | Server and client skill data |
| 4 | Power Guard lasts 30 minutes (now 90 seconds). | agreed | Server and client skill data |
| 5 | Final Attack stays as it is. | agreed | Nothing |

To measure once built: bundling frees many skill points. A Fighter can then max every 2nd job skill, which is not possible today.

### Page (2nd job)

| # | Change | Status | Needs |
|---|--------|--------|-------|
| 1 | Sword and Blunt Weapon Mastery, Booster and Final Attack are each bundled, by the pairing rule. | agreed | Server code |
| 2 | The Boosters last 30 minutes (now 200 seconds) and have no HP cost. | agreed | Server and client skill data |
| 3 | Power Guard lasts 30 minutes (now 90 seconds). | agreed | Server and client skill data |
| 4 | Threaten lowers attack and defence by 30 (now 20). | agreed | Server and client skill data |
| 5 | Final Attack's numbers stay as they are. | agreed | Nothing |

### Spearman (2nd job)

| # | Change | Status | Needs |
|---|--------|--------|-------|
| 1 | Spear and Pole Arm Mastery, Booster and Final Attack are each bundled, by the pairing rule. | agreed | Server code |
| 2 | The Boosters last 30 minutes (now 200 seconds) and have no HP cost. | agreed | Server and client skill data |
| 3 | Hyper Body lasts 30 minutes (now 300 seconds). | agreed | Server and client skill data |
| 4 | Iron Will lasts 30 minutes (now 300 seconds) and gives +40 weapon and magic defence (now +20 each). | agreed | Server and client skill data |
| 5 | Final Attack's numbers stay as they are. | agreed | Nothing |

To note: a permanent Hyper Body makes the Dark Knight line by far the highest-HP class. That fits the class and sets up its later skills, which trade HP for damage.

### Crusader (3rd job)

| # | Change | Status | Needs |
|---|--------|--------|-------|
| 1 | Combo Attack lasts 30 minutes (now 200 seconds). | agreed | Server and client skill data |
| 2 | Panic and Coma are each bundled across sword and axe, by the pairing rule. | agreed | Server code |
| 3 | Panic and Coma use up 3 orbs instead of all of them, so they are worth pressing without giving up all the Combo damage. Robin's choice. | agreed | Server code; to be tested, since the client also shows the orb count |
| 4 | Coma has no HP cost (now 25 HP). | agreed | Server and client skill data |
| 5 | Shout always stuns at max level (now 95%). | agreed | Server and client skill data |
| 6 | Armor Crash, Shield Mastery and Improving MP Recovery stay as they are. | agreed | Nothing |

### White Knight (3rd job)

| # | Change | Status | Needs |
|---|--------|--------|-------|
| 1 | The element charges (fire, ice, lightning) are bundled across sword and blunt weapon, by the pairing rule. | agreed | Server code |
| 2 | The element charges last 30 minutes (now 200 seconds) and all do 130% (now 110 to 125%). | agreed | Server and client skill data |
| 3 | Charged Blow has no HP cost (now 25 HP). | agreed | Server and client skill data |
| 4 | Charged Blow no longer uses up the active charge. In the original game this only comes with Advanced Charge in 4th job. Advanced Charge then needs a different bonus; to settle when we reach the Paladin. | agreed | Server code; to be tested, since the client may remove the charge by itself |
| 5 | Magic Crash, Shield Mastery and Improving MP Recovery stay as they are. | agreed | Nothing |

### Dragon Knight (3rd job)

The class's theme is spending HP for damage. Small constant HP costs are removed; the big deliberate ones stay.

| # | Change | Status | Needs |
|---|--------|--------|-------|
| 1 | Crusher and Dragon Fury are each bundled across spear and pole arm, by the pairing rule. | agreed | Server code |
| 2 | Dragon Fury has no HP cost (now 30 HP). | agreed | Server and client skill data |
| 3 | Dragon Blood lasts 30 minutes (now 160 seconds) and no longer drains HP (now 20 HP every 4 seconds). | agreed | Server and client skill data; the drain is server code |
| 4 | Dragon Roar keeps its 30% HP cost but no longer stuns you for 2 seconds afterwards. | agreed | To be tested: the self-stun may be handled by the client |
| 5 | Crusher's numbers, Sacrifice, Power Crash and Elemental Resistance stay as they are. | agreed | Nothing |

### Shared by all three warrior 4th jobs

| # | Change | Status | Needs |
|---|--------|--------|-------|
| 1 | Power Stance lasts 30 minutes (now 300 seconds). | agreed | Server and client skill data |
| 2 | Achilles reduces damage taken by 20% (now 15%). | agreed | Server and client skill data |
| 3 | Rush, Monster Magnet and Hero's Will stay as they are. Rush is the warrior's real movement skill and only arrives at level 120; if +20 speed on Iron Body feels too slow before that, moving Rush to 3rd job is the next step. | agreed | Nothing |

### Hero (4th job)

| # | Change | Status | Needs |
|---|--------|--------|-------|
| 1 | Brandish, Advanced Combo Attack, Enrage and Guardian stay as they are. The Hero already gains from the crit rule and from permanent Rage and Combo Attack. | agreed | Nothing |

### Paladin (4th job)

| # | Change | Status | Needs |
|---|--------|--------|-------|
| 1 | Holy Charge and Divine Charge are bundled, by the pairing rule. | agreed | Server code |
| 2 | Holy Charge and Divine Charge last 30 minutes (now 300 seconds) and do 150% (now 140%), so they stay ahead of the 3rd job charges at 130%. | agreed | Server and client skill data |
| 3 | Advanced Charge still raises Charged Blow to 350%. Its other half, keeping the charge, moved to 3rd job; in its place Charged Blow hits up to 10 monsters (now 6). | agreed | Server and client skill data; the target count per Advanced Charge level is to be tested |
| 4 | Blast, Heaven's Hammer and Guardian stay as they are. | agreed | Nothing |

**Changes:** none yet.

## Magicians

Fire/Poison, Ice/Lightning, Bishop. Under discussion since 2026-10-10, one job at a time.

**Goal:** not set. Starting point: magicians are not weak overall (they are the best group killers from 3rd job on). The problems are early: 1st job is slow.

**Ideas**

- Stronger bonus against elemental weaknesses.

### Magician (shared 1st job)

| # | Change | Status | Needs |
|---|--------|--------|-------|
| 1 | Magic Guard lasts 30 minutes (now 10). | agreed | Server and client skill data |
| 2 | Magic Armor lasts 30 minutes (now 400 seconds) and gives more defence. It gives +80 weapon defence (now +40) and +40 magic defence (now none). | agreed | Server and client skill data |
| 3 | Energy Bolt hits up to 3 monsters (now 1), so it has a use next to Magic Claw. | agreed | Server and client skill data |
| 4 | Improved MP Recovery recovers more MP. It gives double what it does now. | agreed | To be tested: natural recovery is worked out by the client, so this may have to be done as extra recovery from the server |
| 5 | Magic Claw and Improved MaxMP Increase stay as they are. | agreed | Nothing |

### Fire/Poison Wizard (2nd job)

| # | Change | Status | Needs |
|---|--------|--------|-------|
| 1 | Meditation lasts 30 minutes (now 200 seconds). | agreed | Server and client skill data |
| 2 | Poison Breath hits up to 4 monsters (now 1) and always poisons at max level (now 60%). It is the branch's group attack: weaker upfront than Thunder Bolt, but the poison keeps working. | agreed | Server and client skill data |
| 3 | Teleport costs less MP: 30 MP at level 1 falling to 5 at max (now 60 falling to 13). Applies to all three magician branches. | agreed | Server and client skill data |
| 4 | Fire Arrow, MP Eater and Slow stay as they are. | agreed | Nothing |

### Ice/Lightning Wizard (2nd job)

| # | Change | Status | Needs |
|---|--------|--------|-------|
| 1 | Meditation lasts 30 minutes (now 200 seconds). | agreed | Server and client skill data |
| 2 | Teleport costs less MP, as for the Fire/Poison Wizard. | agreed | Server and client skill data |
| 3 | Cold Beam freezes for 3 seconds at every level (now 1 second at level 1, 2 at max). | agreed | Server and client skill data |
| 4 | Thunder Bolt, MP Eater and Slow stay as they are. | agreed | Nothing |

### Cleric (2nd job)

| # | Change | Status | Needs |
|---|--------|--------|-------|
| 1 | Holy Arrow does 120 magic attack (now 80) and hits up to 3 monsters (now 1). | agreed | Server and client skill data |
| 2 | Bless lasts 30 minutes (now 200 seconds) and also reduces all damage taken by 15%. | agreed | Server and client skill data; the damage reduction is server code |
| 3 | Invincible lasts 30 minutes (now 300 seconds). | agreed | Server and client skill data |
| 4 | Teleport costs less MP, as for the wizards. | agreed | Server and client skill data |
| 5 | Heal and MP Eater stay as they are. | agreed | Nothing |

To measure once built: Bless, Invincible, Magic Guard and a full self-heal together make the cleric the sturdiest 2nd job by a distance.

### Fire/Poison Mage (3rd job)

| # | Change | Status | Needs |
|---|--------|--------|-------|
| 1 | Element Amplification keeps +40% magic damage, and its extra MP cost shrinks as it is levelled, to none at max (now every spell costs double). | agreed | Server and client skill data |
| 2 | Element Amplification also raises the weakness bonus: monsters weak to your element take 175% at max (now 150%). Robin's idea. | agreed | To be tested: the weakness multiplier is probably inside the client program. If so, it is parked. |
| 3 | Spell Booster lasts 30 minutes (now 200 seconds) and has no HP cost. | agreed | Server and client skill data |
| 4 | Poison Mist always poisons at max level (now 70%). | agreed | Server and client skill data |
| 5 | Seal always succeeds at max level (now 95%). | agreed | Server and client skill data |
| 6 | Explosion, Element Composition and Partial Resistance stay as they are. | agreed | Nothing |

### Ice/Lightning Mage (3rd job)

| # | Change | Status | Needs |
|---|--------|--------|-------|
| 1 | Element Amplification: extra MP cost shrinks to none at max, as for the Fire/Poison Mage. | agreed | Server and client skill data |
| 2 | Element Amplification raises the weakness bonus to 175% at max, as for the Fire/Poison Mage. | agreed | To be tested, likely client code |
| 3 | Spell Booster lasts 30 minutes (now 200 seconds) and has no HP cost. | agreed | Server and client skill data |
| 4 | Ice Strike freezes for 3 seconds at every level (now 1 second at level 1, 2 at max). | agreed | Server and client skill data |
| 5 | Seal always succeeds at max level (now 95%). | agreed | Server and client skill data |
| 6 | Thunder Spear, Element Composition and Partial Resistance stay as they are. | agreed | Nothing |

To measure once built: Ice Strike can keep a whole group frozen almost permanently. It is the safest group attack in the game.

### Priest (3rd job)

| # | Change | Status | Needs |
|---|--------|--------|-------|
| 1 | Holy Symbol lasts 30 minutes (now 2) and gives its full +50% exp to a solo player (now only a fraction when alone). | agreed | Server and client skill data, plus the setting `USE_FULL_HOLY_SYMBOL` |
| 2 | Summon Dragon lasts 30 minutes (now 140 seconds). It still uses one Summoning Rock per cast. | agreed | Server and client skill data |
| 3 | Doom always succeeds at max level (now 90%). | agreed | Server and client skill data |
| 4 | Mystic Door lasts 10 minutes (now 3). | agreed | Server and client skill data |
| 5 | Shining Ray, Dispel and Elemental Resistance stay as they are. | agreed | Nothing |

To measure once built: a permanent +50% exp makes the priest level half again as fast as every other class. +25% is the fallback if that proves too much.

### Fire/Poison Arch Mage (4th job)

Maple Warrior at 30 minutes is covered by the rule for all classes.

| # | Change | Status | Needs |
|---|--------|--------|-------|
| 1 | Mana Reflection lasts 30 minutes (now 250 seconds). | agreed | Server and client skill data |
| 2 | Elquines lasts 30 minutes (now 160 seconds). | agreed | Server and client skill data |
| 3 | Infinity lasts 120 seconds (now 40). The 10-minute cooldown stays. | agreed | Server and client skill data |
| 4 | Meteor Shower costs 2,500 MP (now 3,500). | agreed | Server and client skill data |
| 5 | Paralyze does 240 magic attack (now 210). | agreed | Server and client skill data |
| 6 | Big Bang, Fire Demon and Hero's Will stay as they are. | agreed | Nothing |

To measure once built: longer Infinity and a cheaper Meteor Shower make the strongest area attack in the game much easier to spam. Idea for later: Fire Demon weakens monsters to ice, which helps a party member, not the Fire/Poison mage; it could weaken them to fire instead.

### Ice/Lightning Arch Mage (4th job)

| # | Change | Status | Needs |
|---|--------|--------|-------|
| 1 | Mana Reflection lasts 30 minutes (now 250 seconds). | agreed | Server and client skill data |
| 2 | Ifrit lasts 30 minutes (now 160 seconds). | agreed | Server and client skill data |
| 3 | Infinity lasts 120 seconds (now 40). The 10-minute cooldown stays. | agreed | Server and client skill data |
| 4 | Blizzard costs 2,500 MP (now 3,500). | agreed | Server and client skill data |
| 5 | Chain Lightning does 210 magic attack (now 180). | agreed | Server and client skill data |
| 6 | Big Bang, Ice Demon and Hero's Will stay as they are. | agreed | Nothing |

To measure once built: a cheaper Blizzard with a longer Infinity freezes and damages 15 monsters on every cast. It is the safest ultimate in the game.

### Bishop (4th job)

| # | Change | Status | Needs |
|---|--------|--------|-------|
| 1 | Mana Reflection lasts 30 minutes (now 250 seconds). | agreed | Server and client skill data |
| 2 | Bahamut lasts 30 minutes (now 160 seconds). | agreed | Server and client skill data |
| 3 | Infinity lasts 120 seconds (now 40). The 10-minute cooldown stays. | agreed | Server and client skill data |
| 4 | Genesis costs 2,500 MP (now 3,500). | agreed | Server and client skill data |
| 5 | Resurrection works on yourself: when you would die, you are revived on the spot instead. Same 30-minute cooldown. Today it does nothing for a solo player. | agreed | To be tested: whether the server can stop a death as it happens |
| 6 | Angel Ray, Holy Shield, Big Bang and Hero's Will stay as they are. | agreed | Nothing |

**Changes:** none yet.

## Bowmen

Bowmaster, Marksman.

**Goal:** not set.

**Ideas:** none yet.

**Changes:** none yet.

## Thieves

### Rogue (shared 1st job)

| # | Change | Status | Needs |
|---|--------|--------|-------|
| 1 | Double Stab: 160% per hit at max instead of 140%. (Also line 1 of the bandit plan.) | agreed | Server and client skill data |
| 2 | Dark Sight has no speed penalty at any level (now slows by 30 at level 1, none only at max). | agreed | Server and client skill data |
| 3 | Nimble Body: +30 accuracy and +30 avoidability at max (now +20 each), plus +10 speed if a passive can give speed. | agreed | Server and client skill data; the speed part is to be tested |
| 4 | Disorder affects up to 6 monsters (now 1), lowers their attack and defence by 30 (now 20), and lasts 2 minutes (now 1). | agreed | Server and client skill data |
| 5 | Lucky Seven and Keen Eyes stay as they are. | agreed | Nothing |

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
| 6 | Chief Bandit | Pickpocket drops mesos on every hit at max level (now 60%) and lasts 30 minutes (now 180 seconds), so Meso Explosion always has something to explode. Meso Explosion itself is unchanged. | agreed | Server and client skill data |
| 7 | Chief Bandit | Meso Guard lasts 30 minutes (now 120 seconds). | agreed | Server and client skill data |
| 8 | Chief Bandit | Band of Thieves does 250% (now 210%) on 6 monsters. It must stay clearly better than Steal, which does 100% on up to 6. | agreed | Server and client skill data |
| 9 | Chief Bandit | Assaulter dashes 50% further and hits up to 3 monsters in its path. | agreed | To be tested: the dash distance may sit in client code |
| 10 | Chief Bandit | Chakra can be used at any HP (now only below half). | agreed | To be tested |
| 11 | Shadower | Assassinate does full damage without the Dark Sight setup. | agreed | To be tested |
| 12 | Shadower | Boomerang Step hits 6 monsters (now 4). | agreed | Server and client skill data |
| 13 | Shadower | Smokescreen's cooldown is 5 minutes (now 10). | agreed | Server and client skill data |
| 14 | Shadower | Taunt, Shadow Shifter and Venomous Stab stay as they are. | agreed | Nothing |

Parked, because they need changes inside the client program:

| Change | Note |
|--------|------|
| Assaulter usable without a monster to target | Robin would like this. Today the skill needs a target to dash to. Flash Jump covers free movement in the meantime. |
| Dark Sight as a toggle, and any attack leaves it | |
| Boomerang Step on slopes and at ledges | |

To measure once it is built: reliable Pickpocket plus a shorter Smokescreen cooldown make the Shadower much richer and safer than before.

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

Under discussion since 2026-10-10, one job at a time.

**Goal:** not set. Starting point: the assassin is not lagging (Night Lord is among the strongest classes), so the work is on chores and gaps, not damage.

**Plan**

| # | Job | Change | Status | Needs |
|---|-----|--------|--------|-------|
| 1 | Assassin | Claw Booster lasts 30 minutes (now 200 seconds). | agreed | Server and client skill data |
| 2 | Assassin | Haste lasts 30 minutes (now 200 seconds). | agreed | Server and client skill data |
| 3 | Assassin | Drain hits up to 3 monsters (now 1), giving 2nd job a group attack. The healing must not grow with it: the heal counts only one monster per use, as today. | agreed | Server and client skill data; the heal rule is server code |
| 4 | Assassin | Critical Throw, Claw Mastery and Endure stay as they are. | agreed | Nothing |
| 5 | Hermit | Shadow Partner lasts 30 minutes (now 3). It still uses one Summoning Rock per cast. | agreed | Server and client skill data |
| 6 | Hermit | Meso Up lasts 30 minutes (now 2). | agreed | Server and client skill data |
| 7 | Hermit | Avenger does 200% on 6 monsters (now 180%). | agreed | Server and client skill data |
| 8 | Hermit | Flash Jump, Shadow Web, Alchemist and Shadow Meso stay as they are. | agreed | Nothing |
| 9 | Night Lord | Shadow Stars lasts 30 minutes (now 2). To measure once built: this removes almost all star use, which was the class's running cost. 10 minutes is the fallback if that proves too generous. | agreed | Server and client skill data |
| 10 | Night Lord | Triple Throw, Taunt, Shadow Shifter, Venomous Star, Ninja Ambush, Ninja Storm and Hero's Will stay as they are. | agreed | Nothing |

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
