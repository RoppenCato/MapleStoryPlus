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
| 2026-10-11 | Travel dash: the beginner skill Nimble Feet (was a short sprint from 2026-10-10 to 2026-10-11) | +10 to +20 speed for 4 to 12 seconds, 60-second cooldown, costs MP | +10 speed and 10 seconds per level, so +30 for 30 seconds at level 3; 5-minute cooldown; original MP cost. Adds to Haste and other speed buffs. | No (the sprint version was) |
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

| 2026-10-10 | The rest of the agreed number changes (about 45 skills), weapon pairs for warriors, Flash Jump for the bandit line, Drain's heal rule, Dragon Blood without drain | See Class-Changes.md | Installed | No |
| 2026-10-11 | Critical hits for every class, flat | 10% for 150% in 1st job rising to 25% for 170% in 4th (our own earlier version) | 40% for 150% in every job. The bowman's Critical Shot goes from 40% to 50% so bowmen and assassins stay ahead. | No |
| 2026-10-11 | Damage rules for every attack skill (82 skills) | Many skills were close to useless at level 1 (Thunder Bolt: 2 at level 1, 60 at max), and a new job's attack often started below the old one | Level 1 is at least 60% of max. A new job's main attack starts at least 10% above the old job's max; where needed the max was raised (Charged Blow 358%, Assaulter 825%, Cold Beam 110, Thunder Bolt 76, Ice Strike 104, Poison Breath 76, Element Composition 165 and 151, Chain Lightning 234, Shining Ray 165). Crusher hits 3 times at every level. | No |
| 2026-10-11 | Second review pass, after the damage simulator | Magicians at 55 to 65% of the other classes on one monster; the bandit 40% ahead of a Fighter in 2nd job; the Hermit at 76% of a Ranger | Magician single-target spells raised at every job (Fire Arrow 155, Cold Beam 140, Holy Arrow 135, Element Composition 215 and 195, Thunder Spear 210, Shining Ray 200, Paralyze 300, Chain Lightning 280, Angel Ray 320 at max). Savage Blow six hits of 85% at max, Assaulter 561 to 701%. Shadow Partner's shadow at 45 to 70% of skill damage, Avenger 175% at max. | No |

## Jobs and progression

| Date | Change | Before | After | Tested in game |
|------|--------|--------|-------|----------------|
| 2026-10-12 | The Guide on the Trade button | The Trade button did nothing | It opens a window anywhere: where you stand, your job advancement, the trials. The job instructors open the same window. | No |
| 2026-10-12 | Job advancement through trials | Each advancement was a chain of quests, tests and items, different per class, with stat requirements for 1st job | 1st job: choose a class at level 10 (8 for a magician). 2nd job at 30: beat Mano and King Slime. 3rd at 70: any 4 of 13 bosses. 4th at 120: any 4 of 15. Explorers only. | No |
| 2026-10-12 | 4th job basics free | 4th job skills needed skill books and mastery books from bosses | The main attack and Maple Warrior are open to level 10 on advancing. The rest will cost boss tokens (not built yet). | No |
| 2026-10-12 | King Slime in the swamp | Only at the end of the Kerning party quest | Also in The Swamp of Despair I, next to Kerning City | No |
| 2026-10-12 | Area bosses every 15 minutes | Checked every 3 hours | Checked every 15 minutes | No |
| 2026-10-12 | Trial bosses sized for one player | HP from 2,000 (Mano) to 35 million (Black Crow), with no relation to a solo fight | HP set from the damage simulator: about 75 seconds for the two before 2nd job, 100 seconds for most, 5 minutes for the three highest of each band. 30 bosses changed. | No |
| 2026-10-12 | Boss tokens and the 4th job skill shop | 4th job skills needed skill books and mastery books | Trial bosses give tokens (1, 2 or 5 by band, the hardest double, a first kill five times; the endgame bosses 15 to 80). In the Guide a 4th job character raises a skill's limit by ten levels for 10, 20, then 30 tokens. | No |
| 2026-10-12 | `@goals` | | Shows what you still need for your next job | No |

## Travel and guidance

| Date | ID | Change | Before | After |
|------|----|--------|--------|-------|
| 2026-10-10 | T-2 | Tower teleport stones cost mesos | Orbis Tower and Eos Tower stones each used up a rock scroll, which could not be bought or found | 5,000 mesos per jump |
| 2026-10-10 | T-4 (part) | Bots answer whispers and give directions | Bots ignored whispers | Whisper any bot: it chats, knows which monsters drop an item, where monsters live, and the quickest way there from your map. Needs the bot chat window running. |

## Economy

| Date | Change | Before | After | Tested in game |
|------|--------|--------|-------|----------------|
| 2026-10-11 | Basic potions cost half: Red, Orange, White and Blue Potion, Mana Elixir | 50, 160, 320, 200 and 620 mesos | 25, 80, 160, 100 and 310 mesos (never below what a vendor pays for one) | No |
| 2026-10-11 | Monsters under level 30 drop twice the mesos | For example Snail 4 to 6 | Snail 8 to 12. 381 monsters. | No |
| 2026-10-11 | Vendors pay a quarter for equipment | 40% of the shop price | 10% of the shop price. Potions, ores and other items are unchanged. | No |
| 2026-10-11 | Set shops in Free Market rooms 1 and 2 | Every room had random shops; a scroll you needed might not be for sale | Room 1: weapon and accessory scrolls, special scrolls (clean slate, chaos, white), potions, middle throwing stars and bullets, gear for scrolling. Room 2: armour scrolls. Stock never runs out. Scrolls cost 100,000 (100%), 300,000 (60%), 150,000 (10%), 1 million (dark 70%), 2 million (dark 30%); chaos 10 million, white 25 million. | No. The server reports all 41 shops opened. |
| 2026-10-12 | Equipment drops from monsters around its own level | Ordinary monsters dropped equipment of any level; about one item in five from level 80 up only dropped from monsters more than 5 levels above it, and most items had three droppers scattered over the game | No ordinary monster drops equipment more than 5 levels above its own level or more than 20 below. Every item that ordinary monsters drop has at least 3 droppers between 10 levels under and 2 over its level. 1,502 drops removed, 2,077 added. | No |
| 2026-10-12 | Popular hunting spots drop more | No difference between a training map and anywhere else | 46 monsters people actually train on are picked first when an item needs a dropper, and equipment of the right level drops there at 0.15% (0.3% with the drop rate) where the usual is 0.08% | No |
| 2026-10-12 | The first gear drops before level 10 | About one wearable piece on the way to level 10; several level 10 starter items dropped from nothing | Equipment needing level 12 or less drops at 0.4% (0.8% with the drop rate) from snails, slimes, mushrooms, pigs and the other monsters up to level 10: about 6 to 9 pieces for your class by level 10. The plain gear of every class at every level now has at least 3 droppers (84 drops added). | No |
| 2026-10-12 | A gear budget per level | A flat chance per kill: a piece of gear every 12 kills at any level, so about 1,800 pieces between level 51 and 60, some 360 of them wearable by your class | Each monster's chance is set so that a level of training gives about 8 pieces at a popular hunting spot and 5.5 elsewhere, never more than 1 kill in 8. About 80 pieces per ten levels, 15 to 25 of them for your class, 2 to 5 weapons. Replaces the flat 0.15% and 0.4% chances of earlier the same day. | No |
| 2026-10-12 | Every class finds gear everywhere | Pirates found a third of what others found; bowmen almost no weapons at 41-50 and 71-80; nothing useful at 111-120 | Every monster living in numbers drops at least one weapon and two armour pieces per class around its level (1,781 drops added), the classes share a monster's gear equally, and level 100 gear drops from everything above it | No |
| 2026-10-12 | Leveling pace by level | Exp, mesos and drops 2x at every level: about 169,000 kills from 1 to 120, 2,000 to 2,600 a level from 31 to 80 | On top of the 2x, a pace by the player's level (`Settings/Pace.tsv`): 1.5 to level 20, 2.5 to 30, 4 to 50, 5 to 80, 4 after. It multiplies exp, mesos and item chances from ordinary monsters (item chances not from bosses), so a level gives the same mesos and drops in fewer kills: about 40,000 kills from 1 to 120. It never looks at the monster's level. | No |
| 2026-10-12 | Trial bosses give a share of a level | Only the boss's own exp | 30% of a level on the first kill, 5% on later kills, counted at the lower of the boss's level and the player's. | No |
| 2026-10-12 | NX per level corrected | The NX chance was worked out from kills at 1x exp, so a level really gave about 2,500 NX | Worked out from the real kills (world rate and pace): 5,000 NX a level as intended. | No |
| 2026-10-12 | Level 110 and 120 gear from the hardest bosses | The Dragon weapons, the level 110 class sets and the Reverse and Timeless gear dropped from almost nothing; the endgame bosses rolled on level 100 gear | Pianus, Bigfoot, Black Crow and Leviathan drop one weapon and one piece of armour of level 110 on every kill; Papulatus, Zakum, Horntail and Pink Bean one weapon and one piece of armour of level 120 Reverse or Timeless gear. Both pieces are for any class (none aimed at the killer), with no stat below standard. 115 items; ordinary monsters stay at level 100. | No |
| 2026-10-12 | Two guaranteed pieces of gear from every trial boss | Gear dropped about 4 kills in 10, from the boss's own list, for any class; two bosses had none, some only gear far from their level | Every kill: one piece for the killer's class (down to the weapon kind of the job) and one for any class, needing a level within 5 of the boss's gear level, with no stat below the item's standard. On top of the boss's own drops. The 35 bosses of `Trials.tsv`. | No |
| 2026-10-12 | A boss always drops at least one item | Each drop was rolled on its own; 61 bosses could drop nothing but mesos, some nearly 9 times in 10 | If no item comes up, one from the boss's list drops anyway, picked in proportion to its chance | No |
| 2026-10-12 | Scroll prices lowered by a third | 100% 100,000; 60% 300,000; 10% 150,000; dark 70% 1 million; dark 30% 2 million; clean slate 250,000 to 3 million; chaos 10 million; white 25 million | 70,000; 200,000; 100,000; 700,000; 1.4 million; 170,000 to 2 million; 7 million; 17 million. With the gear budget a level at 60 earns about 0.9 million, where the first prices assumed 1.5. | No. The server reports all 41 shops open. |
| 2026-10-12 | Top gear from level 95 keeps dropping | Magicians found no class weapon after level 110: their best ordinary wand needs 98 | Gear needing level 95 or more drops from every ordinary monster above it | No |
| 2026-10-12 | NX from every monster, as a budget per level | 100 NX card 1 kill in 500, 250 NX card 1 in 2,000, the same at every level and for bosses: almost nothing early | The chance follows the monster so that a level of training gives about 5,000 NX (at most every other kill; a 250 NX card a tenth as often). About 28,000 NX by level 15, 108,000 by 30, 313,000 by 70, 570,000 by 120: more than a player needs, on purpose, to try several pets and outfits. A boss counts as ten monsters of its level. Two earlier versions the same day (flat 1 in 200, then 1,500 a level) gave too little. | No |
| 2026-10-12 | Ordinary gear that nothing dropped | About 1,050 equips had no source | 173 of them now drop from monsters around their level: what shops sell, and other colours of items that drop. 859 are left out (event items, quest rewards, and about 171 weapons that need a human eye). | No |
| 2026-10-12 | `@whodrops` and `@whatdropsfrom` for everyone | GM commands | Any player can use them | No |
| 2026-10-12 | A drop site | Nothing; drops had to be looked up in the database | `docs/drops.html`: search any item or monster, with the real chance | Checked in a browser |
 showed that between level 10 and 20 monsters paid about 53,000 mesos while potions cost about 78,000. Now it is about 106,000 against 41,000.

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
