# Game changes

What is different in our game compared to the original, as a player sees it. This is the list to compile "what have we changed" from.

Add a row when a change is done and tested. The ID points to the item in the [Implementation list](Implementation-List.md). Class and skill changes go in [Class-Changes.md](Class-Changes.md) instead.

"Original" here means the SoloMapling server as we copied it on 2026-10-10, which already differs from official MapleStory (2x rates, 1/10 travel time, bots).

## Settings

| Date | ID | Change | Before | After |
|------|----|--------|--------|-------|
| 2026-10-10 | - | Character name filter removed | Names containing any of about 60 blocked words (test, gm, master, party, event...) were refused | Any unused name of 3-12 letters or digits is allowed |

## Skills and movement

Built so far. The full agreed design is in [Class-Changes.md](Class-Changes.md).

| Date | Change | Before | After | Tested in game |
|------|--------|--------|-------|----------------|
| 2026-10-10 | Sprint: the beginner skill Nimble Feet | +10 to +20 speed for 4 to 12 seconds, 60-second cooldown, costs MP | +20 speed for 10 seconds, 20-second cooldown, no MP cost. Adds to Haste and other speed buffs. | Yes |
| 2026-10-10 | Speed cap | 140 | 160 | Yes |
| 2026-10-10 | Haste (bandit and assassin) | 200 seconds at max | 30 minutes at max | Yes |
| 2026-10-10 | Every other booster, class buff, Maple Warrior and summon | 2 to 20 minutes | 30 minutes at max (a few shorter by design, listed in the Development log) | Yes, spot-checked: buffs last far longer than before. Not timed to the full 30 minutes, and not every one of the 85 skills was tried. |

| 2026-10-10 | Critical hits for every class | Only bowmen and assassins could crit | Every other class crits too: 10% for 150% in 1st job, 15% for 150% in 2nd, 20% for 160% in 3rd, 25% for 170% in 4th. Shown as a permanent Sharp Eyes icon. | Yes, on a Crusader |
| 2026-10-10 | Defence buffs | Iron Body and Magic Armor +40 weapon defence; Iron Will +20 | Iron Body and Magic Armor +80 weapon and +40 magic defence; Iron Will +40 of each; Iron Body also +20 speed | Yes (Iron Body) |
| 2026-10-10 | HP costs | Boosters, Slash Blast, Coma, Charged Blow and Dragon Fury cost HP | No HP cost | Yes (Slash Blast, Sword Booster) |
| 2026-10-10 | Rage | -12 weapon defence while active | No penalty | Yes |
| 2026-10-10 | Teleport | 60 MP falling to 13 | 30 MP falling to 5 | Yes |
| 2026-10-10 | Dark Sight | Slows you until maxed | No speed penalty | Yes |
| 2026-10-10 | Other values in the same batch: Threaten and Disorder at -30; Shout, Seal, Doom, Power Knock-Back, Poison Breath, Poison Mist and Pickpocket always work at max; 3-second freezes on Cold Beam and Ice Strike; ultimates at most 2,500 MP; Element Amplification with no extra MP cost at max; Dash +20; full Holy Symbol bonus when alone | See Class-Changes.md | As agreed | Not individually. Same kind of change as the tested ones. |

| 2026-10-10 | Double Stab | 2 hits of 140% at max | 2 hits of 160% at max | Yes |
| 2026-10-10 | Savage Blow | 4 to 6 hits of 40% to 80% | 6 hits at every level, 55% at level 1 to 100% at level 30 | Yes |
| 2026-10-10 | Steal | Hits 1 monster | Hits 4 monsters from level 1 and 6 at max, with its own hit box | Yes |
| 2026-10-10 | Tooltips | Showed the original numbers | Rewritten to show the new numbers for every changed skill. 244 values have no place in their text and are not shown. | Yes |

## Travel and guidance

| Date | ID | Change | Before | After |
|------|----|--------|--------|-------|
| 2026-10-10 | T-2 | Tower teleport stones cost mesos | Orbis Tower and Eos Tower stones each used up a rock scroll, which could not be bought or found | 5,000 mesos per jump |
| 2026-10-10 | T-4 (part) | Bots answer whispers and give directions | Bots ignored whispers | Whisper any bot: it chats, knows which monsters drop an item, where monsters live, and the quickest way there from your map. Needs the bot chat window running. |

## The Hub

| Date | ID | Change | Before | After |
|------|----|--------|--------|-------|

## Quests

| Date | ID | Change | Before | After |
|------|----|--------|--------|-------|

## Scrolls

| Date | ID | Change | Before | After |
|------|----|--------|--------|-------|

## NX and Cash Shop

| Date | ID | Change | Before | After |
|------|----|--------|--------|-------|

## Job progression

| Date | ID | Change | Before | After |
|------|----|--------|--------|-------|

## Bosses

| Date | ID | Change | Before | After |
|------|----|--------|--------|-------|

## Client

| Date | ID | Change | Before | After |
|------|----|--------|--------|-------|
