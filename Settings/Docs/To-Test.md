# To test in the game

Everything that is built but has not been seen working in play. Newest first. When something is tested, tick it and tell Claude, so that the features page and the other docs can say so; if it fails, note what happened next to it.

Before testing: start `Start-Server.bat`, and `Start-Bot-Chat.bat` for anything about bots. Test characters are in [Test-Accounts.md](Test-Accounts.md).

Last updated: 2026-10-12.

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
- [ ] 4th job at 120: main attack and Maple Warrior can be raised to level 10. *Needs a level 120 character; the character tool does not make those yet.*

## 2. Drops (2026-10-12)

- [ ] `@whodrops <item>` and `@whatdropsfrom <monster>` work on an ordinary (non-GM) character.
- [ ] **Starter gear:** a new character sees gear drop about 1 kill in 8 from snails, slimes and mushrooms, and has several wearable pieces by level 10.
- [ ] At level 30 and up, gear drops clearly more rarely than before (about 1 kill in 100 to 400) and feels like an event, not a flood.
- [ ] A popular hunting spot (Wild Boars, Jr. Wraiths, Wolf Spiders ...) drops gear of about your own level.
- [ ] **A boss always drops at least one item.** Kill Mano or Stumpy a few times.
- [ ] The drop site (`docs/drops.html`) matches what a monster drops in the game: pick one monster and compare.

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
