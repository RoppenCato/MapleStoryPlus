/*
 * What the changes page (index.html) shows. This is the only file to edit.
 * Update it in the same commit as any change a player would notice.
 *
 * One entry per change:
 *   title    what it is, in a few words
 *   text     one sentence a player understands
 *   details  optional list of finer points (shown when the entry is opened)
 *   kind     "feature" (new), "tweak" (a change to how the game was), or "fix"
 *   status   "confirmed" (seen working in play), "built" (made, not yet seen in play), or "planned"
 *   date     optional, when it was made
 */
window.CHANGELOG = {
  title: "MapleStoryPlus",
  theme: "maple",             // the look of the page: "arcade", "warcraft" or "maple"
  tagline: "Old MapleStory, made to be played alone in a world that is still full of people.",
  intro: "Everything that is different from the original game (version 83, around 2009), by area. Open an entry for the details. Confirmed means it has been seen working in play; built means it is made but not yet tried.",
  repo: "https://github.com/RoppenCato/MapleStoryPlus",
  updated: "2026-10-11",
  footer: "MapleStoryPlus is a private hobby project. It is not connected to Nexon or Wizet.",

  categories: [
    {
      name: "The world and its bots",
      colour: "#f07d00",
      summary: "Thousands of computer-played characters fill the towns, the training maps and the Free Market, and you can talk to them.",
      items: [
        { title: "A world full of bots", kind: "feature", status: "confirmed",
          text: "About 3,100 computer-played characters train, travel, trade and chat, so no map feels deserted.",
          details: ["This comes with SoloMapling, the server this project is built on.",
                    "The bots are made fresh every time the server starts."] },
        { title: "Bots keep shops in the Free Market", kind: "feature", status: "confirmed",
          text: "Around a hundred bot-run shops sell equipment, scrolls, potions and chairs, with stock and prices that differ from room to room.",
          details: ["Also part of SoloMapling.", "Rooms 1 and 2 now hold our own set shops instead; see Money and shops."] },
        { title: "Whisper a bot and it answers", kind: "feature", status: "confirmed", date: "2026-10-10",
          text: "Send any bot a whisper and it replies like a person playing the game, in its own words.",
          details: ["A small helper window has to be running next to the server for this.",
                    "Nothing about the conversation is saved; a bot forgets it after ten quiet minutes.",
                    "A bot cannot see anything outside the game and will not claim to be anything but a player."] },
        { title: "Bots know drops, monsters and the way there", kind: "feature", status: "built", date: "2026-10-10",
          text: "Ask a bot what drops an item, where a monster lives or how to get somewhere, and it answers from the real game data.",
          details: ["Directions are the quickest route from the map you are standing on, with every boat, taxi and tower teleport named.",
                    "It only brings this up when you ask; small talk stays small talk.",
                    "Fares are left out unless you ask what it costs."] },
        { title: "Every bot is somebody", kind: "feature", status: "built", date: "2026-10-11",
          text: "Each bot is played by one of 300 made-up people with a name, an age, a home town, a job, a temper and things going on in their life.",
          details: ["A bot stays the same person every time you talk to it.",
                    "It knows what time it is where it lives, so someone in Japan may be up in the middle of the night.",
                    "Its mood changes from day to day.",
                    "They write English; a Swede, Norwegian or Dane answers in their own language if you write to them in one of those."] },
        { title: "Bots that remember you", kind: "feature", status: "planned",
          text: "A bot keeps a few notes about earlier talks with you and picks up where you left off." },
        { title: "Bots in your guild and party", kind: "feature", status: "planned",
          text: "Invite bots to your guild, call one to your party, and have them talk in guild and party chat." }
      ]
    },
    {
      name: "Getting around",
      colour: "#2b9fd9",
      summary: "Faster on foot and less waiting, while travel still costs something.",
      items: [
        { title: "Sprint", kind: "feature", status: "confirmed", date: "2026-10-10",
          text: "The beginner skill Nimble Feet is now a sprint for every character: a burst of speed on a short cooldown, free to use.",
          details: ["+20 speed for 10 seconds, 20 seconds between uses, no MP cost.",
                    "It adds to Haste and other speed buffs; normally only the strongest speed buff counts.",
                    "Put it on Shift to run the way most games do."] },
        { title: "Higher speed limit", kind: "tweak", status: "confirmed", date: "2026-10-10",
          text: "The fastest a character can move is 160 where it used to be 140.",
          details: ["Thieves are the fastest: 140 with Haste and 160 while sprinting.", "Other classes reach about 140 while sprinting."] },
        { title: "Tower stones take mesos", kind: "tweak", status: "built", date: "2026-10-10",
          text: "The teleport stones in Orbis Tower and Eos Tower cost 5,000 mesos a jump.",
          details: ["They used to eat a scroll that no shop sold and no monster dropped."] },
        { title: "Short boat and ride times", kind: "tweak", status: "built",
          text: "Boats, trains and other rides take a tenth of their original time.",
          details: ["The plan is to settle on about three minutes, long enough to feel like a journey."] },
        { title: "A travel guide", kind: "feature", status: "planned",
          text: "A way to see where you can go from where you stand and how to get anywhere, without asking a bot." }
      ]
    },
    {
      name: "All classes",
      colour: "#3f9b2f",
      summary: "Rules that apply to every job: long buffs, critical hits for all, fewer annoyances.",
      items: [
        { title: "Buffs last 30 minutes", kind: "tweak", status: "confirmed", date: "2026-10-10",
          text: "Boosters, class buffs, Maple Warrior and summons last 30 minutes at max level.",
          details: ["85 skills changed. Lower skill levels scale up in step and none got shorter.",
                    "A few are shorter on purpose: Puppet, Dash and the Transformations 3 minutes; Infinity and the Octopus turrets 2 minutes; Mystic Door 10 minutes.",
                    "Smokescreen has a 5-minute cooldown.",
                    "Checked on several buffs in play, not on all 85."] },
        { title: "Critical hits for every class", kind: "feature", status: "confirmed", date: "2026-10-10",
          text: "Warriors, magicians, bandits and pirates can now land critical hits too, a little stronger with each job advancement.",
          details: ["1st job: 10% chance for 150% damage.", "2nd job: 15% for 150%.", "3rd job: 20% for 160%.", "4th job: 25% for 170%.",
                    "Bowmen and assassins keep their own, stronger critical skills.",
                    "It shows as a permanent Sharp Eyes icon.",
                    "Seen working on a warrior; not yet checked on a magician."] },
        { title: "Single-target skills that reach more monsters", kind: "feature", status: "confirmed", date: "2026-10-10",
          text: "Five early attacks that used to hit one monster now also damage the monsters standing next to it.",
          details: ["Energy Bolt 3 monsters, Poison Breath 4, Holy Arrow 3, Arrow Blow 3, Drain 3.",
                    "The extra monsters take the same damage as the first, give or take 10%, a moment after the first hit lands.",
                    "They do not play a hit animation of their own."] },
        { title: "No HP cost on boosters and everyday attacks", kind: "tweak", status: "confirmed", date: "2026-10-10",
          text: "Weapon boosters, Slash Blast, Coma, Charged Blow and Dragon Fury no longer take HP to use." },
        { title: "Skills that always work when maxed", kind: "tweak", status: "built", date: "2026-10-10",
          text: "Shout, Seal, Doom, Power Knock-Back, Poison Breath, Poison Mist and Pickpocket succeed every time at max level." },
        { title: "Tooltips show the new numbers", kind: "fix", status: "confirmed", date: "2026-10-10",
          text: "Skill descriptions were rewritten to match every changed skill.",
          details: ["A few hundred values have no place in the original wording and are not shown."] },
        { title: "Cygnus Knights and Aran", kind: "tweak", status: "planned",
          text: "The same design pass for the Cygnus Knights and Aran, who are untouched so far." },
        { title: "No damage limit", kind: "tweak", status: "planned",
          text: "Lift the 199,999 limit on a single hit." }
      ]
    },
    {
      name: "Thieves",
      colour: "#b565d9",
      summary: "Bandits catch up with assassins, and both are quicker on their feet.",
      items: [
        { title: "Double Stab", kind: "tweak", status: "confirmed", date: "2026-10-10",
          text: "Two hits of 160% at max level, up from 140%." },
        { title: "Savage Blow", kind: "tweak", status: "confirmed", date: "2026-10-10",
          text: "Six hits at every level, growing from 55% each to 100% each at max.",
          details: ["It used to start at 4 hits of 40% and end at 6 hits of 80%.", "It is better than Double Stab from the first point."] },
        { title: "Steal hits a group", kind: "tweak", status: "confirmed", date: "2026-10-10",
          text: "Steal hits 4 monsters from the first level and 6 when maxed, with a reach wide enough to catch monsters standing apart." },
        { title: "Dark Sight does not slow you", kind: "tweak", status: "confirmed", date: "2026-10-10",
          text: "The speed penalty of Dark Sight is gone at every level." },
        { title: "Flash Jump for bandits", kind: "feature", status: "built", date: "2026-10-10",
          text: "Chief Bandits and Shadowers get Flash Jump from 3rd job, without spending skill points on it.",
          details: ["Its level follows your own from level 70 and is maxed at 89.",
                    "It is put on a free key for you, because the skill window cannot show another job's skill.",
                    "The jump itself was tried on a bandit and works; getting it automatically has not been tried."] },
        { title: "Nimble Body and Disorder", kind: "tweak", status: "built", date: "2026-10-10",
          text: "Nimble Body gives +30 accuracy and avoidability, and Disorder weakens up to 6 monsters around you by 30 for 2 minutes." },
        { title: "Stronger 3rd and 4th job attacks", kind: "tweak", status: "built", date: "2026-10-10",
          text: "Band of Thieves, Assaulter, Boomerang Step and Avenger hit harder or reach more monsters.",
          details: ["Band of Thieves 250% at max (was 210%).", "Assaulter hits up to 3 monsters and reaches half as far again.",
                    "Boomerang Step hits 6 monsters at max (was 4).", "Avenger 200% at max (was 180%)."] },
        { title: "Drain heals from one monster", kind: "tweak", status: "built", date: "2026-10-10",
          text: "Drain now damages up to 3 monsters but heals from the first one only, so it does not heal three times as much." },
        { title: "Chakra and Assassinate without conditions", kind: "tweak", status: "planned",
          text: "Chakra at any HP and Assassinate without Dark Sight." }
      ]
    },
    {
      name: "Warriors",
      colour: "#e2572b",
      summary: "Tougher, a little faster, and free to switch weapon type.",
      items: [
        { title: "Iron Body is worth taking", kind: "tweak", status: "confirmed", date: "2026-10-10",
          text: "Iron Body gives +80 weapon defence, +40 magic defence and +20 speed at max.",
          details: ["It used to give +40 weapon defence and nothing else.", "Iron Will gives +40 of each defence (was +20)."] },
        { title: "Rage without the drawback", kind: "tweak", status: "confirmed", date: "2026-10-10",
          text: "Rage no longer lowers your weapon defence." },
        { title: "Paired weapon skills", kind: "feature", status: "built", date: "2026-10-10",
          text: "A point in a sword skill also raises its axe twin, so a warrior pays once and can use either weapon.",
          details: ["Fighter: sword and axe mastery, final attack and booster.", "Page: sword and blunt weapon.", "Spearman: spear and pole arm.",
                    "Also Panic and Coma, the element charges, Crusher and Dragon Fury, Holy and Divine Charge."] },
        { title: "Stronger charges", kind: "tweak", status: "built", date: "2026-10-10",
          text: "The White Knight's element charges do 130% at max, and Holy and Divine Charge 150%." },
        { title: "Achilles and Berserk", kind: "tweak", status: "built", date: "2026-10-10",
          text: "Achilles takes 20% off damage at max (was 15%) and Berserk switches on below 60% HP (was 50%)." },
        { title: "Dragon Blood without the HP drain", kind: "tweak", status: "built", date: "2026-10-10",
          text: "Dragon Blood no longer eats 20 HP every four seconds while it is active." },
        { title: "Threaten", kind: "tweak", status: "built", date: "2026-10-10",
          text: "Threaten lowers attack and defence by 30 at max." },
        { title: "Panic, Coma and Charged Blow", kind: "tweak", status: "planned",
          text: "Panic and Coma on 3 orbs, and Charged Blow that keeps its charge and hits 10 monsters." },
        { title: "Aura of the Beholder and Berserk", kind: "tweak", status: "planned",
          text: "The Beholder stops healing you at the Berserk line, so it no longer switches Berserk off." }
      ]
    },
    {
      name: "Magicians",
      colour: "#4f7fd9",
      summary: "Cheaper to move, sturdier, and with a group attack from the start.",
      items: [
        { title: "Cheaper Teleport", kind: "tweak", status: "confirmed", date: "2026-10-10",
          text: "Teleport costs 30 MP at level 1 falling to 5 at max, down from 60 falling to 13." },
        { title: "Magic Armor", kind: "tweak", status: "built", date: "2026-10-10",
          text: "Magic Armor gives +80 weapon defence and +40 magic defence at max (was +40 weapon defence)." },
        { title: "Holy Arrow", kind: "tweak", status: "built", date: "2026-10-10",
          text: "Holy Arrow does 120 magic attack at max, up from 80, and reaches up to 3 monsters." },
        { title: "Freezes last 3 seconds", kind: "tweak", status: "built", date: "2026-10-10",
          text: "Cold Beam and Ice Strike freeze for 3 seconds at every level." },
        { title: "Ultimates cost less MP", kind: "tweak", status: "built", date: "2026-10-10",
          text: "Meteor Shower, Blizzard and Genesis cost at most 2,500 MP.",
          details: ["Element Amplification no longer adds MP cost at max level."] },
        { title: "Paralyze and Chain Lightning", kind: "tweak", status: "built", date: "2026-10-10",
          text: "Paralyze does 240 at max (was 210) and Chain Lightning 210 (was 180)." },
        { title: "Full Holy Symbol when alone", kind: "tweak", status: "built", date: "2026-10-10",
          text: "Holy Symbol gives its whole experience bonus to a priest playing solo." },
        { title: "Bless and Resurrection", kind: "tweak", status: "planned",
          text: "Bless takes 15% off damage, and a Bishop can revive themself." },
        { title: "MP recovery and elemental weakness", kind: "tweak", status: "planned",
          text: "Double natural MP recovery, and a bigger bonus for hitting a monster with the element it is weak to." }
      ]
    },
    {
      name: "Bowmen and pirates",
      colour: "#1fae9a",
      summary: "A little speed for bowmen and real damage for pirates.",
      items: [
        { title: "Bowman speed", kind: "tweak", status: "built", date: "2026-10-10",
          text: "Focus adds +10 speed, and Thrust gives +10 where it used to give +30, so bowmen are steadily a bit faster." },
        { title: "Sniper and Marksman", kind: "tweak", status: "built", date: "2026-10-10",
          text: "The Sniper's Strafe does 120% per arrow at max (was 100%) and Marksman Boost gives +15 attack (was +10)." },
        { title: "Pirate attacks hit harder", kind: "tweak", status: "built", date: "2026-10-10",
          text: "Double Shot, Invisible Shot, Grenade and Rapid Fire all do clearly more damage.",
          details: ["Double Shot 130% per bullet at max (was 80%).", "Invisible Shot 200% (was 170%).", "Grenade 200% (was 140%).", "Rapid Fire 200% (was 170%)."] },
        { title: "Pirate attacks reach more monsters", kind: "tweak", status: "built", date: "2026-10-10",
          text: "Corkscrew Blow, Backspin Blow, Invisible Shot, Blank Shot and Energy Blast hit up to 6 monsters.",
          details: ["They used to hit 3, and Energy Blast 4."] },
        { title: "Dash", kind: "tweak", status: "built", date: "2026-10-10",
          text: "Dash gives +20 speed and lasts 3 minutes." },
        { title: "Battleship, capsules and Snipe", kind: "tweak", status: "planned",
          text: "A Battleship that survives longer, Flamethrower and Ice Splitter without capsules, and Snipe that is worth using on bosses." }
      ]
    },
    {
      name: "Money and shops",
      colour: "#d9a400",
      summary: "An easier start, scrolls you can always buy, and mesos that still mean something late in the game.",
      items: [
        { title: "Double experience, mesos and drops", kind: "tweak", status: "built",
          text: "Monsters give twice the experience, twice the mesos and drop items twice as often; bosses drop five times as often." },
        { title: "Basic potions at half price", kind: "tweak", status: "built", date: "2026-10-11",
          text: "Red, Orange, White and Blue Potions and Mana Elixirs cost half as much in every shop.",
          details: ["25, 80, 160, 100 and 310 mesos (were 50, 160, 320, 200 and 620).",
                    "An estimate of the first 30 levels showed potions costing more than monsters paid."] },
        { title: "More mesos from early monsters", kind: "tweak", status: "built", date: "2026-10-11",
          text: "Every monster under level 30 drops twice the mesos it used to, on top of the doubled rate.",
          details: ["Early income no longer depends on a lucky equipment drop."] },
        { title: "Set shops in Free Market rooms 1 and 2", kind: "feature", status: "built", date: "2026-10-11",
          text: "Two Free Market rooms hold shops that always have every ordinary scroll in stock, at prices that never move.",
          details: ["Room 1: weapon and accessory scrolls, special scrolls, potions, throwing stars and bullets, gear for scrolling.",
                    "Room 2: armour scrolls, one or two shops per piece of armour.",
                    "100% scrolls 100,000 mesos, 60% 300,000, 10% 150,000.",
                    "Dark scrolls 1 million (70%) and 2 million (30%).",
                    "Clean slate scrolls 250,000 to 3 million, chaos scroll 10 million, white scroll 25 million.",
                    "Elixirs, Power Elixirs, All Cure Potions and the attack pills.",
                    "Wolbi, Mokbi, Kumbi and Tobi stars and three kinds of bullets. The best stars are left out on purpose: those still come from monsters.",
                    "Work Gloves, capes, bathrobes, earrings and shields to scroll.",
                    "The other twenty rooms keep their random bot shops."] },
        { title: "Shopkeepers pay less for equipment", kind: "tweak", status: "built", date: "2026-10-11",
          text: "Selling weapons and armour to a shop gives a quarter of what it used to; everything else sells as before.",
          details: ["Selling every equipment drop added up to hundreds of millions of mesos by level 120, which made prices meaningless."] },
        { title: "A token for 4th job books", kind: "feature", status: "planned",
          text: "Bosses give a token that buys 4th job skill books and mastery books from a character in the Free Market.",
          details: ["Every boss on the way up gives some and the hardest give the most."] },
        { title: "Bosses pay more mesos", kind: "tweak", status: "planned",
          text: "Bosses become the best way to earn the mesos that scrolls cost." }
      ]
    },
    {
      name: "Screen and comfort",
      colour: "#e0457b",
      summary: "The old game on a modern screen, with fewer hoops at the start.",
      items: [
        { title: "High resolution and ultrawide", kind: "feature", status: "confirmed", date: "2026-10-10",
          text: "The game runs at a modern resolution and fills an ultrawide screen where the original was fixed at 800 by 600.",
          details: ["Done with the MapleEzorsia v2 add-on for the original game.", "Played at 1680 by 720, which a 3440 by 1440 screen shows at exactly twice the size."] },
        { title: "Fewer forbidden character names", kind: "fix", status: "built", date: "2026-10-10",
          text: "The server no longer refuses names that merely contain words like test, master or party.",
          details: ["The game itself still has its own list and refuses some names, Test among them. That part is not changed."] },
        { title: "No terms screen for new accounts", kind: "tweak", status: "built", date: "2026-10-10",
          text: "A new account goes straight to the game without the agreement screen." }
      ]
    },
    {
      name: "Still to come",
      colour: "#6b8e23",
      summary: "The larger plans: a solo progression through bosses, a hub, and quests of our own.",
      items: [
        { title: "Trials: a solo path through the bosses", kind: "feature", status: "planned",
          text: "The game is split into bands of levels, each with six to eight boss trials of which you must beat four to move on.",
          details: ["Levels still come mainly from training.", "Beating a trial again keeps paying.", "Party quests are added later."] },
        { title: "Job advancement through the trials", kind: "tweak", status: "planned",
          text: "2nd, 3rd and 4th job and their skills are earned through that progression in place of the old quests and skill book hunts." },
        { title: "A boss outside every starting town", kind: "feature", status: "planned",
          text: "The first band: one boss near each of the explorer towns." },
        { title: "Bosses made for one player", kind: "tweak", status: "planned",
          text: "Boss health, attacks, rewards and respawn times reworked so each can be beaten alone at the right level." },
        { title: "A hub", kind: "feature", status: "planned",
          text: "One place for the things a solo player keeps coming back to: goals, travel, storage, boss status." },
        { title: "Quests of our own", kind: "feature", status: "planned",
          text: "Repeatable hunting and boss quests with a board to pick them up from and a way to see your progress." },
        { title: "Cash shop basics without paying", kind: "feature", status: "planned",
          text: "A pet that picks up items, extra inventory slots and the like, earned in play." }
      ]
    }
  ]
};
