# Research: bots and bosses

First pass for `R-1`, `R-2` and `R-3` in the [Implementation list](Implementation-List.md). Done 2026-10-10 by reading the server code and its documentation. **Nothing here is tested in the game yet.**

## Short answer

- Bots are decoration that can also fight. They are not a replacement for real party members in content that needs players to do things.
- You can recruit bots as companions that follow you, share party exp and deal real damage, also to bosses.
- The big bosses are locked behind "expeditions" that need 3 to 6 real players to sign up. One setting drops that to 1.
- Party quests need 3 to 6 players and have puzzle stages. Bots can only play one of them (Orbis PQ). The rest need to be made solo, or skipped.

So the likely direction is: **make the content soloable, and use companion bots as extra damage and company, not as a requirement.**

## How the bots work (`R-1`)

About 3,100 bots are created every time the server starts (2,536 of them are training bots out in the hunting maps). They are real characters to the game, but:

- They are wiped and recreated at every server start.
- They have no real inventory and do not affect the economy. Their loot pickups are for show.
- Far from any player they do almost nothing: no attacks, no movement. They gain levels by a formula instead. When you enter their map they switch to real fighting.

| Bot type | Where | What it does |
|----------|-------|--------------|
| Training bots | Hunting maps | Grind monsters, move on to harder maps as they level |
| Town bots | Henesys, Ellinia, Perion, Kerning, Sleepywood, Orbis, El Nath | Wander, sit, chat, react to players |
| Social bots | Towns | Talk with you through a small menu; can be recruited |
| Merchant bots | Free Market (Henesys, Ludibrium, Perion, El Nath) | Run shops with generated stock and prices; buy, sell, haggle |
| Game bots | Henesys Game Zone | Blackjack, dice, a drop-racing game, Gachapon |
| Jump quest bots | Henesys Pet Park | Attempt the jump quest |
| OPQ bots | Orbis PQ lobby | Recruit, party up and play Orbis Party Quest |
| Tutorial bot | Maple Island | Greets new players, can grant GM powers and starter gear |
| Scrolling bots | Towns | Scroll items for show |

## Companion bots (`R-3`)

This is the part that matters for solo play.

- **How:** talk to a social bot in a town or a training bot in the field and ask it to party. It accepts about 70 to 80% of the time; a refusal has a 3 minute cooldown. The bot must be level 10 or higher.
- **What it does:** follows you everywhere, across maps and portals, and fights next to you. Party exp is shared for real.
- **Damage:** real damage to monsters, rolled from the bot's job and level (not from gear). A 3rd job bot hits for thousands per line. The attack code has special handling for bosses, with Zakum's arms named.
- **Buffs:** bots cast their class buffs (for example a cleric's Bless).
- **How many:** a party holds 6, so up to 5 companions. The world-wide limit is 30.
- **Ending it:** tell it to "train here" and it stays as a training bot. If you leave or the party ends, it goes back to being a normal bot.

Not known yet, to test in game:

- Whether bots take damage or can die. Likely not, since monster hits are reported by a real game client and bots have none.
- Whether companions follow you into boss rooms and party quest maps.
- Whether a bot in your party counts toward the "minimum players" of a party quest.

## Bosses and group content (`R-2`)

### Expedition bosses

These need players to sign up at an NPC. Bots cannot sign up.

| Boss | Players needed | Minimum level |
|------|----------------|---------------|
| Balrog (easy) | 3 | 50 |
| Balrog | 6 | 50 |
| Zakum | 6 | 50 |
| Showa boss | 3 | 100 |
| Scarga | 6 | 100 |
| Horntail | 6 | 100 |
| Chaos Zakum | 6 | 120 |
| Chaos Horntail | 6 | 120 |
| Pink Bean | 6 | 120 |
| Crimsonwood Keep PQ | 6 | 90 |

The setting `USE_ENABLE_SOLO_EXPEDITIONS` (now off) changes "players needed" to 1 for all of them. It also lets you skip prequests in some NPC scripts (Zakum and Horntail entry among them). Once inside, the fight only ends early if the last player leaves.

That makes entry possible. It does not make the fights winnable alone: HP and attacks are unchanged. That is section 10 (`B`) of the plan.

### Party quests

Each has its own minimum, and most have stages where several players must stand on things or collect items.

| Party quest | Players needed | Level |
|-------------|----------------|-------|
| Henesys PQ | 3 | 10+ |
| Kerning PQ | 3 | 21-30 |
| Ludibrium PQ | 5 | 35-50 |
| Ellin PQ | 4 | 44-55 |
| Orbis PQ | 5 | 51-70 |
| Ludibrium Maze PQ | 3 | 51-70 |
| Pirate PQ | 3 | 55-100 |
| Magatia PQ | 4 | 71-85 |
| Amoria PQ | 6 | 40+ |
| Horntail PQ (prequest) | 6 | 120+ |
| Guild Quest | 6 | any |

There is no single setting for these. Each is a script with its own number. Lowering the number is easy; making the puzzle stages work for one player is real work per quest.

### Bosses with no entry requirement

Area bosses and bosses reached by walking in (Mushmom, Jr. Balrog, Papulatus, Pianus and similar) were not checked in this pass. They have no player-count gate in the expedition list, but some have quest or item requirements. To be listed in `B-1`.

## What this means for the plan

1. **Decision (end of section 1):** solo by default, with companions as optional help. Recommended.
2. **Quick win `Q-2`:** turn on solo expeditions. Then test one boss entry alone.
3. **Test companions early:** recruit a few, take them to a boss, and answer the three unknowns above. If they hold up, boss tuning (`B-3`) can assume "you plus a few bots" instead of "you alone", which keeps bosses closer to the original.
4. **Party quests:** decide per quest whether to make it solo, leave it for bots (Orbis PQ only), or drop it.
