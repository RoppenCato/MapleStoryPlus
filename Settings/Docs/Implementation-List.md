# Implementation list

The order we do things in. Tick items off as they are done. Each item has an ID (for example `T-2`) so the change lists can point back to it.

When an item changes the game, also record it in:

- [Game-Changes.md](Game-Changes.md): what is different from the original game, as a player sees it.
- [Class-Changes.md](Class-Changes.md): everything about classes and skills.
- [Development-Log.md](Development-Log.md): which server files were changed.

## Why this order

1. Get it running and backed up before changing anything.
2. Learn how the bots and bosses work before designing around them.
3. Take what the settings file already gives us.
4. Travel and the hub come before rewards, because scrolls, NX and quests need a place to live.
5. The quest system comes before scrolls and NX, because it is one of the ways to earn them.
6. Job progression and classes come before bosses, because boss tuning depends on how strong the classes are.

The order is a plan, not a rule. Move things when it makes sense.

---

## 0. Foundation

- [x] `F-1` Copy the server (SoloMapling) and set up folders
- [x] `F-2` Install Java 21 and MySQL, build and start the server
- [x] `F-3` Choose a client (original v83 + MapleEzorsia v2) and download the files
- [x] `F-4` Install the client and log in for the first time
- [x] `F-5` Make our character a GM so we can test things
- [x] `F-6` Ultrawide: 1680x720 in fullscreen (Alt+Enter). Details in `Client/README.md`.
- [ ] `F-7` Raise the damage cap in the client and confirm the server accepts it
- [ ] `F-8` Backups: private GitHub repo for code and settings, and a database backup script
- [ ] `F-9` Run the server's own tests once

## 1. Understand what we have (no changes)

- [ ] `R-1` How the bots work: which types exist, where they go, what they can do with a real player
- [ ] `R-2` Bosses solo: which bosses need a party or expedition, a prequest, or several players in practice
- [ ] `R-3` Can bots join a party or help on a boss, or must every boss be made soloable?
- [ ] `R-4` How skills are stored and what it takes to change one. Suspected: both the server data and the client data must be edited, and giving a class another class's skill needs a client edit. Confirm with one test skill.
- [ ] `R-5` How NPC scripts, shops, drops and quests are stored, so we know what is easy and what is hard
- [ ] `R-6` Play the unchanged game for a while and note what feels bad solo

Decision after this section: **is everything made solo, or do bots fill the party?** Most later sections depend on it.

## 2. Quick wins from the settings file

These need no code. Current values are in [Settings/README.md](../README.md).

- [ ] `Q-1` Decide exp, meso and drop rates (now 2x / 2x / 2x, boss drops 5x)
- [ ] `Q-2` Solo expeditions (`USE_ENABLE_SOLO_EXPEDITIONS`, now off). Note: it also skips the Zakum prequest.
- [ ] `Q-3` Boat and ride times (`travel_rate`, now 10, meaning 1/10 of the normal time). Target: about 3 minutes.
- [ ] `Q-4` Pets: never hungry (`PETS_NEVER_HUNGRY`, now off), auto-potion settings
- [ ] `Q-5` Go through the rest of the settings file once and pick what we want

## 3. Travel and guidance

Goal: you still take boats and travel the world, and it stays immersive, but it is quicker and you always know your options.

- [ ] `T-1` Boats and other rides take about 3 minutes (see `Q-3`)
- [ ] `T-2` Tower travel (Orbis Tower, Eos Tower and similar) costs meso instead of scrolls
- [ ] `T-3` List every travel route in the game: from, to, how, cost, time
- [ ] `T-4` Guidance: a way to see where you can go from here and how to get somewhere. Design to decide (an NPC in every town, a command, a world map item).
- [ ] `T-5` Decide what stays slow on purpose

## 4. The Hub

Goal: one place with everything needed for solo play, where bots do not go.

- [ ] `H-1` Choose the place: the Free Market or another map
- [ ] `H-2` Decide what is in it (scroll access, NX basics, quest board, travel guide, boss status, storage, job help)
- [ ] `H-3` Decide how you get there (a UI button, an NPC in every town, an item)
- [ ] `H-4` Keep bots out of it
- [ ] `H-5` Rework the Free Market and the UI buttons we are not using
- [ ] `H-6` Build the first version with one or two NPCs, then add to it as later sections are done

## 5. Custom quest system

Goal: kill monsters and bosses for rewards. One of the main ways to earn scrolls and NX.

- [ ] `C-1` Design: quest types (kill X monsters, kill a boss, collect items), daily or repeatable, level ranges
- [ ] `C-2` Design the rewards and how they connect to scrolls (`S`) and NX (`N`)
- [ ] `C-3` Where you pick them up (quest board in the Hub)
- [ ] `C-4` Build the tracking and a first set of quests
- [ ] `C-5` Add boss quests once bosses are reworked (`B`)

## 6. Scrolls

Goal: you can scroll weapons and gear efficiently. Not free and not effortless, so a good result still feels good.

- [ ] `S-1` Map out how scrolls are obtained today (drops, shops, quests, gachapon, bot merchants)
- [ ] `S-2` Decide the source: a shop for a currency, quest rewards, better drops, or a mix
- [ ] `S-3` Decide the effort: what it costs to scroll one item fully
- [ ] `S-4` Decide scroll rules (success chances, slots lost on failure, chaos scrolls, white scrolls). Settings exist for some of this.
- [ ] `S-5` Build it and test with one weapon from start to finish

## 7. NX

Goal: earning NX feels rewarding. The basics, such as pet looting, are easy to get.

- [ ] `N-1` List what counts as basics (pet, pet loot gear, storage and inventory slots)
- [ ] `N-2` Decide how the basics are given (starter pack, early quest, cheap in the Hub)
- [ ] `N-3` Decide how NX is earned (quests, bosses, drops, playtime) and how much
- [ ] `N-4` Review Cash Shop prices and contents against that income
- [ ] `N-5` Build it

## 8. Job progression

Goal: advancing jobs works for a solo player. The original third and fourth job, and skill books in particular, do not.

- [ ] `J-1` Map out the current path: levels, quests and items for every job advancement
- [ ] `J-2` Map out skill books and mastery books: which skills need them and where they come from
- [ ] `J-3` Decide the new progression: which levels, what you must do, what replaces skill books
- [ ] `J-4` Build it for one class as a test
- [ ] `J-5` Roll it out to all classes

## 9. Classes and skills

Goal: classes feel balanced and fun. Damage and costs are reviewed, and classes may get new or changed skills.

Details per class are in [Class-Changes.md](Class-Changes.md).

- [ ] `K-1` Set the method from `R-4`: how a skill change is made, tested and recorded
- [ ] `K-2` Agree on a baseline: what "balanced" means (damage per second at set levels, mobbing, survivability, mobility)
- [ ] `K-3` Go through each class: discuss, set a goal, write the plan
- [ ] `K-4` Implement class by class, ticking off in Class-Changes.md

## 10. Bosses

Goal: bosses are meaningful and fun progression, and all of them can be killed.

- [ ] `B-1` List every boss: level, HP, attacks, drops, spawn time, entry requirements
- [ ] `B-2` Decide the progression order and at what level each boss should be beatable
- [ ] `B-3` Rework HP, attacks and levels to match the classes after section 9
- [ ] `B-4` Rework drops so each boss gives something worth having
- [ ] `B-5` Rework spawn times
- [ ] `B-6` Boss status: a way to see that a boss is up (in the Hub, a message, or both)

---

## Ideas not placed yet

Add things here as they come up, then move them into a section.

- Faster movement for everyone, or Shift as a sprint key. Options: raise base speed and the client's speed cap (simple), a sprint toggle skill on Shift (server work), true hold-to-sprint (needs a client code change). Ties in with the warrior speed idea.
- Remove the client's built-in forbidden name list (needs a WZ editor on `Etc.wz`). Postponed.
- New accounts skip the terms message: code is changed, takes effect at the next server rebuild.
