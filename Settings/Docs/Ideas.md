# Ideas

Things we might do. Nothing here is decided or planned. When an idea is picked up, it moves into the [Implementation list](Implementation-List.md) and gets an ID.

Each idea has a status: `new`, `looked into`, `planned` (moved to the Implementation list) or `dropped`.

Class and skill ideas live in [Class-Changes.md](Class-Changes.md).

---

## Bots

### Guild and party

| Idea | Status | Notes |
|------|--------|-------|
| Invite bots to your guild. They keep existing, stay in the guild, and can be invited again at any time. | new | Today all bots are wiped and recreated at every server start, with new names and looks. This needs a set of bots that are saved and brought back. |
| Inviting a guild bot to your party teleports it to your location. | new | Companion bots already follow you across maps once they are in your party. The new part is fetching one from anywhere. |

### Bots that talk (LLM)

| Idea | Status | Notes |
|------|--------|-------|
| Hook up a cheap Claude model that answers when you whisper a bot or mention its name in chat. | new | The server already routes chat to bots and has scripted replies, so there is a place to plug this in. Needs an Anthropic API key, costs a little per message, and replies take a second or two. The key must never go into the public GitHub repo. |
| Give each bot a simple backstory as a basis for the model: age, gender, profession, type of humour, mood today, hobbies and so on. | new | Bots already get a generated look, level and gear when they are created; a personality sheet would be generated the same way. It only stays consistent if the bot itself is saved, which ties in with the guild idea above. |

#### How it should work (Robin's design, 2026-10-10)

1. You whisper a bot, or mention a bot in a chat.
2. You get connected to that bot through Claude Haiku.
3. Haiku is loaded with the bot's backstory and its history.
4. You chat. The conversation stays open as long as the chat lasts.
5. When the chat ends (the player logs out, or the bot is kicked from the party), the conversation is summarized by a set of rules and added to the bot's history.
6. Next time, the same thing happens with the updated history.

#### How it could be built

- **A chat bridge in its own window**, started next to the server. The game server sends it chat lines; it sends replies back. The window shows every exchange.
- **One Claude Code session per conversation**, running Haiku on the subscription login, with no tools and a short "you are this character" instruction. The session holds the conversation while it lasts, so each line is quick to send. An API key can replace the subscription later without a rebuild.
- **One small file per bot** holding the backstory and the history. This is what Haiku is loaded with.
- **Bots only call Claude when spoken to.** Scripted lines stay for everything else.

#### Things the design needs to settle

- **More ways a chat ends:** you walk away and say nothing more (an idle timeout), or the server stops. Lines should be saved to disk as they happen, so a crash does not lose the conversation before it is summarized.
- **Summary rules:** what is kept (what the bot learned about you, promises, how it feels about you) and a size limit. Old entries need merging, or the history grows without end.
- **Saved bots first:** a history only makes sense for a bot that still exists after a restart. Same foundation as the guild idea.
- **Mentions:** how a name in chat is matched to a bot, and what happens when two bots are mentioned or several players talk to the same bot.
- **Which bots:** all 3,000, only town and social bots, or only the ones in your guild or party.
- **Limits:** how many conversations at once, and whether there is a cap on usage.

**Prototype built 2026-10-10:** whisper any bot, no saving or history. See `Bot-Chat-Bridge.py` in [Scripts](../Scripts/README.md). Works in the game: replies arrive as whispers in 2 to 4 seconds. Next steps would be saved bots, history with summaries, and mentions in normal chat.

---

## Shops and economy

### A fixed room in the Free Market (Robin, 2026-10-11)

One Free Market room has set shops that always sell what a player needs, so scrolling does not depend on luck in the random shops. The other rooms stay random.

- Each spot is a shop of its own with a plain title: weapon scrolls, overall scrolls, top and bottom scrolls, and so on.
- Both normal scrolls (10%, 60%, 100%) and dark scrolls (30%, 70%) are sold. Dark scrolls cost more.
- Paid in mesos. No tokens: bosses give more mesos instead, plus their chance at good drops.
- Stock is always there and prices are fixed in a list we control.

To settle: which room, the price level, whether chaos, clean slate and white scrolls are sold, and what else the room sells besides scrolls.

## Movement and travel

| Idea | Status | Notes |
|------|--------|-------|
| Faster movement for everyone, or Shift as a sprint key. | planned | Three routes: raise base speed and the client's speed cap; turn the beginner skill Nimble Feet into a sprint (more speed, longer, no cooldown, bound to Shift); or true hold-to-sprint, which needs a client code change. Decided 2026-10-10: Nimble Feet becomes the sprint. Numbers and the speed budget are in Class-Changes.md under "All classes". |

Travel changes that are already planned (ride times, meso for towers, guidance) are in section 3 of the Implementation list.

---

## Client and display

| Idea | Status | Notes |
|------|--------|-------|
| Remove the client's built-in forbidden name list, so names like "Test" work. | looked into | Needs a WZ editor on the client's `Etc.wz`. Postponed. The server-side filter is already removed. |
| Fix the slow Alt+Tab in fullscreen. | looked into | Two untested options: tune Magpie's settings, or try the dgVoodoo2 graphics wrapper. |
| Start the game directly in fullscreen. | looked into | Setting it in `config.ini` was followed by a start-up error, so it is back to window mode plus Alt+Enter. Cause not confirmed. |

---

## Accounts and quality of life

| Idea | Status | Notes |
|------|--------|-------|
| New accounts skip the terms message. | looked into | The code is changed. It takes effect at the next server rebuild. |

---

## Tools

| Idea | Status | Notes |
|------|--------|-------|
| Fourth job support in the character tool (levels 120 to 200). | new | Needs fourth job builds and mastery levels set, since most fourth job skills need a mastery book. |
