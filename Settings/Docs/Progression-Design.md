# Progression design

How a solo player moves through the game: trials, tokens, job advancement and skill points. This is a design in progress. Nothing here is built yet.

Related: [Bosses and party quests](Bosses-and-Party-Quests.md), [Class changes](Class-Changes.md), [Implementation list](Implementation-List.md) sections 5, 8 and 10.

## Decided

| Topic | Decision | Date |
|-------|----------|------|
| Structure | The game is split into level bands. Each band has about 6 to 8 trials; completing 4 finishes the band. | 2026-10-10 |
| Levels | Levels still come mainly from hunting. Trials are not the main source of exp. | 2026-10-10 |
| Repeats | Repeating a boss or party quest gives something. | 2026-10-10 |
| Tokens | Trials give tokens. Tokens buy things, skill books among them, so the player chooses what to get first. | 2026-10-10 |
| Scope | Bosses first. Party quests are added later. | 2026-10-10 |
| Jobs | Job advancement comes from this progression instead of the original advancement quests. | 2026-10-10 |

## Proposed, not decided

### Job levels: 10 / 30 / 60 / 100

Third job moves from level 70 to 60, and fourth job from 120 to 100.

| | Original | Proposed | Stronger squish (not recommended) |
|---|---|---|---|
| 1st job | 10 | 10 | 10 |
| 2nd job | 30 | 30 | 30 |
| 3rd job | 70 | 60 | 50 |
| 4th job | 120 | 100 | 80 |

Why 60 / 100 and not 50 / 80:

- The bands line up with where the bosses are: plenty of bosses sit between 30 and 60, and between 60 and 100.
- Each job still lasts long enough to enjoy: 20, 30, 40 and then 100 levels.
- At 50 / 80 the player gets fourth job skills while gear and hunting maps are still made for second and third job, which makes everything after it trivial.

### Skill points

Skill points keep coming every level, but the amount per level changes so each job still gets about as many points as before in fewer levels.

| Job | Original | Proposed |
|-----|----------|----------|
| 1st (10 to 30) | 3 per level, 61 in all | 3 per level, 61 in all |
| 2nd (30 to 60) | 3 per level over 40 levels, 121 in all | 4 per level over 30 levels, 121 in all |
| 3rd (60 to 100) | 3 per level over 50 levels, 151 in all | 4 per level over 40 levels, 161 in all |
| 4th (100 to 200) | 3 per level over 80 levels, 241 in all | 3 per level over 100 levels, 301 in all |

### Skills that are useless at low level

Skills like Savage Blow only become worth using after many points. Two ways to fix it, which can be combined:

1. **Head start (server only):** on job advancement, the main attack skill is granted at a useful level for free.
2. **Rescale the skill (server and client data):** change the skill's level table so level 1 is already usable and later levels add less. This belongs to the class work.

### Bands and trials (bosses only for now)

| Band | Levels | Finishing it gives | Candidate bosses |
|------|--------|--------------------|------------------|
| 1 | 10 to 30 | 2nd job | Mano (20). Very few bosses exist below level 30, so this band needs other trials or lower-level bosses. |
| 2 | 30 to 60 | 3rd job | Stumpy (35), Deo (38), Seruf (45), Rombot (47), Faust (50), Giant Centipede (50), King Clang (55), Shade (56), Timer (59), Mushmom (60) |
| 3 | 60 to 100 | 4th job | Zombie Mushmom (65), Dyle (65), Zeno (65), Nine-Tailed Fox (70), Tae Roon (71), Riche (74), King Sage Cat (77), Jr. Balrog (80), Eliza (83), Chimera (85), Snowman (90), Balrog |
| 4 | 100 and up | Endgame rewards | Griffey (105), Manon (105), Pianus (110), Leviathan (120), Papulatus (125), Zakum, Horntail, Pink Bean |

### Tokens

- One token type. Higher bands give more per kill.
- First kill of a boss: a large one-time amount. Repeat kills: a smaller amount, limited per day so farming one easy boss is not the best plan.
- The token shop has sections that open as bands are finished, so early tokens cannot buy endgame items.
- Shop contents: skill books and mastery books, scrolls, and NX basics. This is also how scrolls (section 6) and NX (section 7) of the Implementation list could be delivered.

### Keeping track

- A trial board NPC in the Hub: shows each band, what is done and what is left, and gives the band reward.
- A chat command, `@goals`, for a quick look anywhere.
- A message on a first kill and when a band is finished.
- Bots can answer "what should I do next?".

### Balance

Set a target fight length and work backwards from measured damage: about 1 to 3 minutes for an ordinary trial boss and 5 to 10 for a band's hardest, for a solo character at the right level in normal gear. The character tool builds that test character.

## To find out first

- Does the client accept third job skills on a level 60 character and fourth job skills at level 100? The server decides job changes, but the client may have its own level checks. Test with one character before building anything on it.
- Which item can serve as the token without client edits (an existing, unused item with a fitting name).
- What Band 1 uses for trials, given how few bosses exist below level 30.
