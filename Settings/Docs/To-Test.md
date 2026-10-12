# To test in the game

Everything that is built but has not been seen working in play. Newest first. When something is tested, tick it and tell Claude, so that the features page and the other docs can say so; if it fails, note what happened next to it.

Before testing: start `Start-Server.bat`, and `Start-Bot-Chat.bat` for anything about bots. Test characters are in [Test-Accounts.md](Test-Accounts.md).

Last updated: 2026-10-12.

## Questions for Robin

Things Claude decided alone and would like a yes or a different number on. None of them blocks anything.

1. **How long should a boss fight be?** The trial bosses are now sized for one player: about 75 seconds for the two before 2nd job, 100 seconds for an ordinary one, 5 minutes for the three highest of each band. Mano went from 2,000 HP to 18,400; Pianus from 30 million to 2.9 million. Longer, shorter?
2. **King Slime in the party quest** is the same monster as the one in the swamp, so he also has 28,600 HP there (was 8,000). Fine, or should the party quest keep the old one?
3. **Tokens.** A boss gives 1 (before 2nd job), 2 (before 3rd), 5 (before 4th), the three hardest of a band double; a first kill gives 5 times that; Leviathan 15, Papulatus 20, Zakum 40, Horntail 60, Pink Bean 80. Raising a 4th job skill's limit by ten levels costs 10, then 20, then 30. A whole 4th job comes to roughly 450 to 550 tokens: about a hundred kills of a level 100 boss, or far fewer of the big ones. Right size of grind?
4. **NX.** Answered 2026-10-12: it should be more, and usable while levelling for pets and gear. Then: there should be more than you need, to try several pets and outfits. Now about 5,000 NX per level (28,000 by level 15, 57,000 by 20, 108,000 by 30, 313,000 by 70, 570,000 by 120), with bosses worth ten monsters. Still to judge in play: is 5,000 a level right? It is `NX_PER_LEVEL` in `Server/src/main/java/plus/NxDrops.java`.
5. **Weapons nothing drops.** 173 pieces of ordinary gear with no source now drop (what shops sell, and other colours of things that drop). 859 are still left out, and about 171 of those are weapons that look ordinary (Gladius, Doombringer, Holy Spear, Black Scarab, Golden Crow ...) mixed with event weapons (Celestial Staff, Andromeda Bow, the Xaru set). Sorting them needs a human eye: should Claude make a list for you to tick?
6. **Boomerang Step** now starts below Assaulter's maximum (600% against 701%), which breaks the "new job beats old" rule for Shadowers. Raise it, or is Assaulter the odd one out?
7. **4th job balance** (simulated, with rough assumptions): Dark Knight far ahead, Bishop and Buccaneer behind. Worth a pass like the one for magicians?
8. **Zakum, Horntail and Pink Bean** give tokens but cannot be fought alone yet. Leave them as a goal for later?
9. **Area bosses every 15 minutes** (all 27, not only the trial ones). Good, or too easy to farm?
10. **Leveling pace.** You asked for faster than my first proposal. Now a rate by level on top of the 2x (`Settings/Pace.tsv`: 1.5 to level 20, 2.5 to 30, 4 to 50, 5 to 80, 4 after), about 40,000 kills from 1 to 120, my guess 27 to 40 hours. Is that the right speed, and does any stretch feel too fast or too slow?

## 1. Job advancement and the Guide (2026-10-12)

Most important: this replaces how every explorer advances.

- [ ] **Trade button** opens the Guide window anywhere. *If nothing happens, the game may not send that button with trading off; the Guide then has to go on another button or a command.*
- [ ] The first page shows your name, level, job, and why you cannot advance yet.
- [ ] **1st job:** a level 10 beginner can choose a class (a magician at level 8). No stat requirement.
- [ ] **Kill Mano** (Thicket Around the Beach III, near Lith Harbor): the message "Trial beaten: Mano. 1 of 2 for 2nd job" appears.
- [ ] The Trials page ticks Mano off.
- [ ] **King Slime** stands in The Swamp of Despair I, next to Kerning City, and can be killed. Level 40, 8,000 HP.
- [ ] After both, at level 30: the Guide offers the 2nd job branches, and choosing one works.
- [ ] **A job instructor** (for example Dances with Balrog in Perion) opens the same window.
- [ ] `@goals` prints what is still needed.
- [ ] A killed area boss is back within 15 minutes.
- [ ] 3rd job at 70 after any 4 band 2 bosses. *To skip the fights: ask Claude to mark trials as beaten for a test character.*
- [ ] 4th job at 120: main attack and Maple Warrior can be raised to level 10. *Ask Claude for a level 120 test character with the trials marked as beaten.*
- [ ] **Boss HP:** Mano takes about a minute at level 20 to 25 and no longer dies in seconds. Try one band 2 boss at its level: about a minute and a half.
- [ ] **Tokens:** killing a trial boss prints "+N boss tokens", five times as many on the first kill, and the Guide's first page shows the total.
- [ ] **4th job skill shop** (4th job character): the Guide's third page lists your skills with their limits and prices; buying one raises the limit by ten and takes the tokens.

## 2. Drops (2026-10-12)

- [ ] `@whodrops <item>` and `@whatdropsfrom <monster>` work on an ordinary (non-GM) character.
- [ ] **Starter gear:** a new character sees gear drop about 1 kill in 8 from snails, slimes and mushrooms, and has several wearable pieces by level 10.
- [ ] At level 30 and up, gear drops clearly more rarely than before (about 1 kill in 100 to 400) and feels like an event, not a flood.
- [ ] A popular hunting spot (Wild Boars, Jr. Wraiths, Wolf Spiders ...) drops gear of about your own level.
- [ ] **Boss gear:** a boss on the trials list (Mano, Stumpy ...) drops two pieces of gear every time, of about its own level: one your class can wear, with the kind of weapon your job uses, and one for any class. Compare a piece with the same item in a shop or from a monster: no stat is lower.
- [ ] **Level 110 and 120 gear:** Pianus, Bigfoot, Black Crow or Leviathan drops one weapon and one piece of armour of level 110 (Dragon weapons, Blue Dragon / Garina / Canopus / Red Hunter sets); Papulatus, Zakum, Horntail or Pink Bean drops one Reverse or Timeless weapon and one piece of armour. Each for any class, not aimed at yours. Check the items look and equip right: the Reverse and Timeless ones come from a later version of the game.
- [ ] **A boss that is not on the list always drops at least one item.**
- [ ] The drop site (`docs/drops.html`) matches what a monster drops in the game: pick one monster and compare.
- [ ] **Leveling pace:** `@rates` shows the pace at your level (1.5 under 21, 2.5 to 30, 4 to 50, 5 to 80, 4 after). A monster gives its exp times 2 times that pace; mesos and drops go up the same. With `Make-Character.py` characters at 25, 45 and 70, count roughly how many kills a level takes: about 130, 420 and 480.
- [ ] **Boss exp:** the first kill of a trial boss gives 30% of a level (of the boss's level if you are above it), later kills 5%.
- [ ] **NX cards:** on a low character an NX card drops about every other kill; around level 50 about 1 kill in 10. Picking it up adds NX (check in the Cash Shop). A level gives roughly 5,000 NX. A boss always drops one.
- [ ] Can the NX actually be spent? Buy a pet in the Cash Shop with NX earned from cards.

## 3. The GM and bot chat (2026-10-12)

- [ ] **Whisper GMNova** although nobody of that name is online: the whisper is accepted and an answer arrives, shown as from a GM.
- [ ] Ask it something about the server ("how much is a chaos scroll"): right answer.
- [ ] Talk for a while, wait five minutes, close and reopen the bot chat window, whisper again: it remembers something about you.
- [ ] Whisper an ordinary bot: short answers in its own voice; "where do i find steelies" gives a real monster; "where should I train at 35" names real places.
- [ ] A reply is never cut in the middle of a sentence.

## 4. Shops and money (2026-10-11 and 12)

- [ ] **Free Market room 1 and 2:** the set shops are there, each opens, and shows 16 items or fewer at the listed prices (60% scroll 200,000, chaos scroll 7 million).
- [ ] Buying a scroll takes the mesos and the amount left stays full.
- [ ] A set of throwing stars bought there is a full stack.
- [ ] Red Potion costs 25 mesos in an ordinary shop.
- [ ] Selling a weapon or armour to a shop gives a quarter of what it used to.
- [ ] Monsters under level 30 drop noticeably more mesos.

## 5. Classes and skills (2026-10-10 and 11)

- [ ] **Travel dash (Nimble Feet):** +30 speed for 30 seconds, 5-minute cooldown, adds on top of Haste.
- [ ] **Crit:** a warrior, bandit or pirate crits about 4 hits in 10. **Do magicians crit?** Cast Fire Arrow twenty times. *This decides whether the magician numbers come down by a tenth.*
- [ ] **Extra targets:** Energy Bolt, Poison Breath, Holy Arrow, Arrow Blow and Drain each damage monsters next to the first (only one of the five has been confirmed).
- [ ] **Level 1 skills:** a skill with one point does about 60% of its maxed damage (try Thunder Bolt or Cold Beam at level 1).
- [ ] **Magician spells:** Fire Arrow, Cold Beam and Holy Arrow feel clearly stronger (155, 140, 135 at max).
- [ ] **Savage Blow:** six hits of 85% at max. **Assaulter** hits for about 700% and reaches 3 monsters.
- [ ] **Shadow Partner:** the shadow does 70% of a skill's damage at max. **Avenger** 175%.
- [ ] **Warrior weapon pairs:** on DevPage, a point in Sword Mastery also raises the blunt weapon mastery.
- [ ] **Flash Jump for bandits:** DevBandit (Chief Bandit) has Flash Jump on a key without being given it by hand, and it grows with level.
- [ ] **Drain** heals from one monster only.
- [ ] **Dragon Blood** no longer drains HP. **Holy Symbol** gives its full bonus alone.
- [ ] Bowman and pirate changes (Strafe for the Sniper, Double Shot, Invisible Shot, Grenade, Rapid Fire, six-target attacks) on DevHunter, DevBrawler and DevGunner.
- [ ] Skills that always work when maxed: Shout, Seal, Doom, Power Knock-Back, Poison Mist, Pickpocket.
- [ ] Tooltips show the new numbers for the skills above.

## 6. Other (2026-10-10 and 11)

- [ ] **Tower stones** in Orbis Tower and Eos Tower take 5,000 mesos.
- [ ] A new account goes in without the terms screen.
- [ ] The test characters made after a server start can be logged into (DevPage, DevCleric, DevHunter, DevBrawler, DevGunner).
- [ ] Companions: ask a bot to party; does it follow, fight and share experience? Does it take damage, and does it follow into a boss map?

## Already confirmed in play

Sprint and the speed limit of 160 (the sprint has since become the travel dash above), 30-minute buffs, Iron Body, Rage, cheaper Teleport, Dark Sight without the slow, no HP cost on boosters, Double Stab, Steal on a group, crit on a warrior, the extra targets as a mechanism, whispering a bot, the HD and ultrawide client.
