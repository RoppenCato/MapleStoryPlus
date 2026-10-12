# Progression design

How a solo player moves through the game: trials, tokens, job advancement and skill points. This is a design in progress. Nothing here is built yet.

Related: [Bosses and party quests](Bosses-and-Party-Quests.md), [Class changes](Class-Changes.md), [Implementation list](Implementation-List.md) sections 5, 8 and 10.

> **Changed 2026-10-11:** the trial token is dropped. Scrolls and other supplies are bought with mesos in a fixed Free Market room (see [Ideas](Ideas.md)), and bosses pay more mesos than now, next to their normal drops. One token is kept, for 4th job skill books and mastery books only. Every boss on the way up gives some, and the hardest bosses give the most, so getting good enough for them pays off. Where the rows and the Tokens section below speak of a trial token or of tokens buying scrolls, they no longer apply.

## Job advancement: decided and built 2026-10-12

Robin's answers to the questionnaire, and what was built from them. Not tested in game yet.

| Question | Decision |
|---|---|
| What you must do to advance | Reach the level and beat 4 of the band's bosses (the trials). |
| Where | The Trade button opens the Guide anywhere. The job instructors open the same window. |
| 4th job skills | The main attack and Maple Warrior are open to level 10 on advancing. Everything else is earned with boss tokens. |
| Band 1 (2nd job) | The two bosses that exist at that level: Mano and King Slime, both. |

| Job | Level | Trials |
|---|---|---|
| 1st | 10 (8 for a magician) | None: choose a class in the Guide. No stat requirements. |
| 2nd | 30 | Mano and King Slime, both. |
| 3rd | 70 | Any 4 of 13: Stumpy, Deo, Seruf, Rombot, Faust, Giant Centipede, King Clang, Shade, Timer, Mushmom, Zombie Mushmom, Dyle, Zeno. |
| 4th | 120 | Any 4 of 15: Nine-Tailed Fox, Tae Roon, Riche, King Sage Cat, Jr. Balrog, Eliza, Chimera, Snowman, Male Boss, Headless Horseman, Griffey, Manon, Pianus, Bigfoot, Black Crow. |

- A boss can be beaten at any level and counts for good, so trials can be done early.
- Reaching the level without the trials: you keep levelling in your old job until they are done.
- The killer gets the credit, and so do party members on the same map.
- King Slime only lived at the end of the Kerning party quest, which one player cannot enter, so he also appears in the swamp next to Kerning City (The Swamp of Despair I).
- Area bosses used to be checked every 3 hours. Now every 15 minutes, so a trial is not a three-hour wait. This applies to every area boss.
- Only explorers. Cygnus Knights and Aran advance the way they always did.
- The original advancement quests still exist but are no longer needed.

Built: the Guide, the kill record, advancement, `@goals`, King Slime in the swamp, the 4th job basics.

Not built yet: the tokens and the 4th job skill shop; boss tuning for one player (several band 3 bosses have tens of millions of HP); a first-kill reward.

Where it lives: `Settings/Trials.tsv` (the bosses per band), `Server/src/main/java/plus/Trials.java` (the rules and every text), `Server/scripts/npc/plusGuide.js` (the window), table `plus_trials` (who has beaten what).

## Decided

| Topic | Decision | Date |
|-------|----------|------|
| Structure | The game is split into level bands. Each band has about 6 to 8 trials; completing 4 finishes the band. | 2026-10-10 |
| Levels | Levels still come mainly from hunting. Trials are not the main source of exp. | 2026-10-10 |
| Repeats | Repeating a boss or party quest gives something. | 2026-10-10 |
| Tokens | Trials give tokens. Tokens buy things, skill books among them, so the player chooses what to get first. | 2026-10-10 |
| Scope | Bosses first. Party quests are added later. | 2026-10-10 |
| Jobs | Job advancement comes from this progression instead of the original advancement quests. | 2026-10-10 |
| Job levels | No level squish. Jobs stay at 10, 30, 70 and 120, and skill points stay at 3 per level. | 2026-10-10 |
| Weak low-level skills | Skills that are useless until many points are spent (Savage Blow and similar) are fixed later, in the class work, not through levels or skill points. | 2026-10-10 |
| Token shop | Tokens buy scrolls and other useful items. | 2026-10-10 |

## Proposed, not decided

### Bands and trials (bosses only for now)

| Band | Levels | Finishing it gives | Candidate bosses |
|------|--------|--------------------|------------------|
| 1 | 10 to 30 | 2nd job | Mano (20), plus one low-level boss outside each starting town. See below. |
| 2 | 30 to 70 | 3rd job | Stumpy (35), Deo (38), Seruf (45), Rombot (47), Faust (50), Giant Centipede (50), King Clang (55), Shade (56), Timer (59), Mushmom (60), Zombie Mushmom (65), Dyle (65), Zeno (65) |
| 3 | 70 to 120 | 4th job | Nine-Tailed Fox (70), Tae Roon (71), Riche (74), King Sage Cat (77), Jr. Balrog (80), Eliza (83), Chimera (85), Snowman (90), Griffey (105), Manon (105), Pianus (110), Balrog |
| 4 | 120 and up | Endgame rewards | Leviathan (120), Dodo (121), Papulatus (125), Lilynouch (131), Lyka (141), Zakum, Horntail, Pink Bean |

### Band 1: one boss outside each starting town (parked 2026-10-10)

Robin's idea: one boss per starter zone, just outside each explorer town, so Band 1 has six bosses to pick 4 from. The game data already has low-level versions of several bosses, so no new monsters are needed. Not tested in game; the matching below is a first guess.

| Town | Boss | Level | HP in the data | Spawn command to try it |
|------|------|-------|----------------|-------------------------|
| Lith Harbor | Mano | 20 | 2,000 | already lives there |
| Henesys | Mushmom (small version) | 10 | 1,000 | `!spawn 9303004` |
| Kerning City | King Slime | 20 | 945 | `!spawn 9500168` |
| Ellinia | King Slime (stronger) or a demon | 23 to 25 | 2,500 to 5,000 | `!spawn 9500325` |
| Perion | Jr. Balrog (small version) | 30 | 3,094 | `!spawn 9500169` |
| Nautilus | A demon: Andras, Amdusias, Crocell, Marbas or Valefor | 25 | 2,500 | `!spawn 9400609` to `9400613` |

Still to do when this is picked up: see how each one looks and fights, settle which boss goes with which town, raise HP to a real boss fight, and write a spawner script per boss.

What the server can and cannot do with bosses:

- Easy: put any existing monster on any map with a respawn timer, and change its HP, exp and drops.
- Needs client edits: a brand-new monster, a different name or level on screen, and how hard a boss hits.

### Tokens

Two kinds:

| Token | Comes from | Buys |
|-------|------------|------|
| Trial token | Every trial boss. Higher bands give more per kill. | Scrolls and other useful items. NX basics could go here too. |
| Mastery token | Band 4 bosses only (level 120 and up). | 4th job skill books and mastery books. |

- First kill of a boss: a large one-time amount. Repeat kills: a smaller amount, limited per day, so farming one easy boss is not the best plan.
- The trial token shop has sections that open as bands are finished, so early tokens cannot buy endgame items.
- Why a separate mastery token: skill books cannot be farmed from easy bosses, and the player never has to choose between scrolling gear and getting core class skills.

### Keeping track

- A trial board NPC in the Hub: shows each band, what is done and what is left, and gives the band reward.
- A chat command, `@goals`, for a quick look anywhere.
- A message on a first kill and when a band is finished.
- Bots can answer "what should I do next?".

### Balance

Set a target fight length and work backwards from measured damage: about 1 to 3 minutes for an ordinary trial boss and 5 to 10 for a band's hardest, for a solo character at the right level in normal gear. The character tool builds that test character.

## To find out first

- Which two items can serve as the tokens without client edits (existing, unused items with fitting names).

## Considered and dropped

| Idea | Why dropped | Date |
|------|-------------|------|
| Level squish: 3rd job at 60 and 4th job at 100 (or 50 and 80), with more skill points per level | Robin chose to keep the original job levels and fix weak skills directly instead. | 2026-10-10 |
