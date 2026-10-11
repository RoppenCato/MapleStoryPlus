# Bots: who they are

The files here describe the people behind the bots. They were made in the WowPlus project and copied here on 2026-10-11. Nothing in them is about one game, so the same files serve both; only the style file is per game.

They are used when you whisper a bot (`Settings/Scripts/Bot-Chat-Bridge.py`).

| File | What it is | Edit it? |
|---|---|---|
| `People.json` | The people: 300 of them, one per line. Each has a first name, gender, age, home with country, language and time zone, occupation, home life, temper, humour, two hobbies, a way of talking, a typing habit, a gaming habit, how experienced they are, something going on in their life, and three favourite topics. | Yes, by hand, one person at a time. Restart the bridge afterwards. |
| `Traits.json` | The lists people are put together from. | Yes. Then run `python Settings/Scripts/Make-Bot-People.py` to add people from the new lists. It keeps the people already there and only adds missing ones (`--count 500` for more, `--fresh` to start over). |
| `Styles/maplestory.md` | How chat sounds in MapleStory: its words, its nicknames for places, its tone. | Yes. Works at once. |

What is personal to this PC is kept outside the repository:

| File | What it is |
|---|---|
| `Database/BotChat/Assignments.json` | Which person plays which bot. Fixed the first time a bot is whispered, so a bot stays the same person even when `People.json` grows. To give a bot a particular person, put that person's `id` here under `maplestory`. |

## What a bot knows about itself

- Who it is: everything on its line in `People.json`.
- What time it is at home, from its time zone. A Japanese player may say it is the middle of the night there.
- Its mood, which changes per day.
- It writes English. A Swede, Norwegian or Dane answers in their own language only when you write to them in a Scandinavian language.

## Not copied from WowPlus

| Thing | Why not |
|---|---|
| Memory (notes about you, what the bot said lately) | Here nothing about a conversation is saved, as decided earlier. Can be added the same way later. |
| Bots that know each other outside the game | Only matters when several bots talk in one chat (guild, party). |
| `Topics.md` (things bots bring up by themselves) | Bots here only answer whispers; they do not start talking. |
| `Styles/wow.md` | The other game. |

## Keeping the two projects the same

The files are copies. If `People.json` or `Traits.json` changes in one project, copy it to the other so the same person plays in both.
