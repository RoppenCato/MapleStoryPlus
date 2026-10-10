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
| Job levels | No level squish. Jobs stay at 10, 30, 70 and 120, and skill points stay at 3 per level. | 2026-10-10 |
| Weak low-level skills | Skills that are useless until many points are spent (Savage Blow and similar) are fixed later, in the class work, not through levels or skill points. | 2026-10-10 |
| Token shop | Tokens buy scrolls and other useful items. | 2026-10-10 |

## Proposed, not decided

### Bands and trials (bosses only for now)

| Band | Levels | Finishing it gives | Candidate bosses |
|------|--------|--------------------|------------------|
| 1 | 10 to 30 | 2nd job | Mano (20). Very few bosses exist below level 30, so this band needs other trials or lower-level bosses. |
| 2 | 30 to 70 | 3rd job | Stumpy (35), Deo (38), Seruf (45), Rombot (47), Faust (50), Giant Centipede (50), King Clang (55), Shade (56), Timer (59), Mushmom (60), Zombie Mushmom (65), Dyle (65), Zeno (65) |
| 3 | 70 to 120 | 4th job | Nine-Tailed Fox (70), Tae Roon (71), Riche (74), King Sage Cat (77), Jr. Balrog (80), Eliza (83), Chimera (85), Snowman (90), Griffey (105), Manon (105), Pianus (110), Balrog |
| 4 | 120 and up | Endgame rewards | Leviathan (120), Dodo (121), Papulatus (125), Lilynouch (131), Lyka (141), Zakum, Horntail, Pink Bean |

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
- What Band 1 uses for trials, given how few bosses exist below level 30.

## Considered and dropped

| Idea | Why dropped | Date |
|------|-------------|------|
| Level squish: 3rd job at 60 and 4th job at 100 (or 50 and 80), with more skill points per level | Robin chose to keep the original job levels and fix weak skills directly instead. | 2026-10-10 |
