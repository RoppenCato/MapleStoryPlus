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

Open questions for this group:

- Which bots get a personality: all 3,000, only town and social bots, or only the ones in your guild?
- Should a bot remember earlier conversations with you?
- Is there a monthly spending limit?

---

## Movement and travel

| Idea | Status | Notes |
|------|--------|-------|
| Faster movement for everyone, or Shift as a sprint key. | looked into | Three routes: raise base speed and the client's speed cap; turn the beginner skill Nimble Feet into a sprint (more speed, longer, no cooldown, bound to Shift); or true hold-to-sprint, which needs a client code change. Nimble Feet is the favourite. Ties in with the warrior speed idea. |

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
