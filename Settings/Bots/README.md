# Bots: who they are

The files here describe the people behind the bots: their lives, their voices and how they type. They are made in the WowPlus project and shared with this one. Nothing in them is about one game; only the style file is.

They are used when you whisper a bot (`Settings/Scripts/Bot-Chat-Bridge.py`). What a bot is made of, part by part, and how to judge whether it sounds real, is in [Character-Sheet.md](Character-Sheet.md). Read that first.

| File | What it is | Edit it? |
|---|---|---|
| `People.json` | The facts for 300 people, one per line: name, age, home and time zone, language, work, home life, temper, humour, hobbies, gaming habit. | Yes, one person at a time. Restart the bridge afterwards. |
| `Traits.json` | The lists people are put together from. | Yes. Then run `python Settings/Scripts/Make-Bot-People.py`. |
| `Backgrounds/<id>.json` | A person written in full: life story, the people around them, small true details, opinions, something going on that moves along every two weeks, how they type, twelve sample lines. | Yes. Change the sample lines and the bot's voice changes with them. |
| `Character-Sheet.md` | Every part of a character, where it is kept, and the listening test. | Shared with WowPlus. |
| `Styles/maplestory.md` | How chat sounds in MapleStory: its words, its short names for monsters and maps, its tone. This project's own. | Yes. Works at once. |
| `Topics.md` | Things bots bring up by themselves. Not used here yet: bots only answer whispers. | |
| `Reference/` | The WowPlus bridge and its listening test, for reading. Not run here. | No. |
| `Update-From-WowPlus.md` | The note that came with the last copy from WowPlus. | No. |

The code that knows who the bots are is `Settings/Scripts/bot_minds.py`. It is the same file in both projects and must stay identical: if this game needs something from it, add an argument, not a second version.

What is personal to this PC is kept outside the repository, in `Database/BotChat`:

| File | What it is |
|---|---|
| `Assignments.json` | Which person plays which bot. Fixed the first time a bot is whispered. To give a bot a particular person, put that person's `id` here under `maplestory`. |
| `maplestory/<you>/GMNova.json` | What the GM remembers about you: up to eight notes and its last ten lines. A plain file; edit or delete it to change or wipe that memory. |
| `_session/` | An empty folder the Claude runs happen in. |
| `_test/` | The listening test's throwaway folder. |

## How a whisper is answered

1. The game server sends the whisper, the bot's level, job and map, and your map to the bridge.
2. The bridge finds the person who plays that bot. The first time a bot speaks, that person is written in full in the background (about a minute); until then the bot answers from the facts alone.
3. If you asked about the game, the bridge looks it up: which monsters drop an item, where a monster lives, where to train at a level, the quickest way somewhere. The answer is handed to the bot as something it knows, so it says it in its own voice.
4. Claude Haiku writes the reply as that person. The length of the answer is drawn, hello, goodbye and thanks get the person's own word, and a joke, a question back or a word about their own day each depend on dice.
5. The person's typing habits (lower case, no apostrophes, their own laugh word) are applied once more in code, and the reply is cut into lines of at most 70 characters.

## The GM: the one who remembers

One name can always be whispered, whether or not anyone of that name is online: **GMNova**, the server's game master. The GM is a person like the others (one of the 300, with a life and a voice), and differs from an ordinary bot in three ways:

- **It can always be reached.** The game server answers a whisper to that name itself; no character has to exist.
- **It knows this server.** It is told everything on the features page (`docs/changes.js`), with the numbers, on top of the drop, monster, training and route knowledge every bot has. So the features page is also what the GM knows: keep it right.
- **It remembers you.** After a talk (eight new lines, or four quiet minutes) Claude Haiku brings its notes about you up to date: at most eight, under 110 characters each, including what it told you about itself. After one remembered talk it is at ease with you; after three it counts you as a friend and its own life comes up.

It only talks: it does not hand out items, mesos or levels, and says so if asked.

Ordinary bots remember the conversation for ten quiet minutes and nothing after that. They are made fresh at every server start, and neither the game's buddy list nor its guilds can hold them, so there is nothing in the game to hang a lasting memory on. (A version where bots became "buddies" inside the bridge only was built on 2026-10-12 and taken out the same day for that reason.)

| To change | Where |
|---|---|
| The GM's name | `GM_NAME` in `Server/src/main/java/soloMapling/BotChat/BotChatBridge.java` (or start the server with `-Dbot-chat-gm=Name`). At most 12 letters, and not a name a bot can get. |
| Who the GM is | Put another person's `id` under `maplestory` → `gmnova` in `Database/BotChat/Assignments.json`. |
| What the GM remembers about you | `Database/BotChat/maplestory/<your character>/GMNova.json`. Edit it, or delete it to start over. |
| What the GM knows about the server | `docs/changes.js`. |

Try it without the game:

```
python Settings/Scripts/Bot-Chat-Bridge.py --gm --say "hey" --say "how much is a chaos scroll" --remember
```

## Writing people in full

```
python Settings/Scripts/Make-Bot-Backgrounds.py --count 20      the next 20 people that have none
python Settings/Scripts/Make-Bot-Backgrounds.py --playing       everyone who already plays a bot
python Settings/Scripts/Make-Bot-Backgrounds.py --ids 4 17      these people, again
python Settings/Scripts/Make-Bot-Backgrounds.py --show 17       print one person as a bot is told about itself
```

## Listening test

After changing the rules in the bridge, the style file or a background, listen before playing:

```
python Settings/Scripts/Test-Bot-Voices.py                six people answer the same eight lines
python Settings/Scripts/Test-Bot-Voices.py --ids 2 6 12   these people
python Settings/Scripts/Test-Bot-Voices.py --friend       the same, as people who count you as a friend
python Settings/Scripts/Test-Bot-Voices.py --talk 6       a short conversation with one person
python Settings/Scripts/Test-Bot-Voices.py --say "..."    your own line
```

What to listen for is in the character sheet. What listening changed here, on top of the rules taken from WowPlus:

| Change | Why |
|---|---|
| "Where should I train at 35" gets real monsters from the game data. | All six answered "not sure" in the same words. |
| Not knowing is said a different way each time. | "Not sure" six times over. |
| A fact answer names one or two monsters, says nothing about the bot's own day and gives no route unless asked. | Answers ran to three lines and ended with the bot's headache. |
| A message that had to be cut ends at a full stop or comma, never on "and". | Half sentences reached the game. |
| "Do not ask a question" also removes a tacked-on "you" at the end. | The question mark went but the question stayed. |
| "im a level 30 cleric" is not a question about where to train. | It was answered with where the Maple Hat drops. |
| No advice when you tell them something ("stay out of its room"). | Helpdesk. |
| A thing is said once per talk. | The same headache came up three times. |

## Not taken over from WowPlus yet

| Thing | What it would need here |
|---|---|
| Memory for every bot, and bots that become friends. | Something in the game to tie it to. Bots are remade at every start and cannot be on the buddy list or in a guild; if bots are ever kept between starts, the WowPlus memory can be used as it is. |
| Bots speaking first: a greeting, a remark of their own. | The game server has to ask for it, and here it only passes on whispers. New server code. |
| Bots that know each other outside the game. | Only matters once several bots talk in one chat. |

## Keeping the two projects the same

Copy in both directions when they change: `People.json`, `Traits.json`, `Backgrounds/`, `Character-Sheet.md`, `bot_minds.py`, `Make-Bot-Backgrounds.py`, `Make-Bot-People.py`. A person then lives the same life in both games.
