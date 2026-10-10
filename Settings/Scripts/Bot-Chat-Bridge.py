"""Bot chat bridge: lets bots answer whispers through Claude Haiku.

The game server sends each whisper to a bot here; this window asks Claude for the bot's reply and
sends it back. Start it with Start-Bot-Chat.bat and leave the window open while you play.

Prototype rules:
  - any bot can be whispered
  - nothing is saved: a bot's personality and the conversation live only while this window is open,
    and a conversation is forgotten after 10 minutes of silence
  - replies come from Claude Code running Haiku on your Claude login (no API key)

Test without the game:   python Settings/Scripts/Bot-Chat-Bridge.py --say "hey, how's the hunt?"
"""
import argparse
import glob
import io
import os
import random
import re
import subprocess
import sys
import threading
import time
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from urllib.parse import parse_qs

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(os.path.dirname(HERE))
PORT = 8585
MODEL = "haiku"
IDLE_SECONDS = 10 * 60          # a conversation is forgotten after this much silence
MAX_TURNS_KEPT = 12             # how many earlier lines the bot still sees
MAX_LINES = 2                   # lines per reply
MAX_LINE_LENGTH = 70            # characters per chat line
REPLY_TIMEOUT = 75
MAX_AT_ONCE = 3                 # conversations answered at the same time

AGES = ["16", "19", "22", "24", "27", "31", "35", "42"]
MOODS = ["cheerful", "tired after a long day", "a bit bored", "excited about a recent drop", "grumpy about bad luck",
         "relaxed", "restless", "in a silly mood"]
HUMOURS = ["dry and sarcastic", "goofy", "dad jokes", "teasing", "deadpan", "barely jokes at all"]
JOBS_IRL = ["student", "warehouse worker", "nurse", "barista", "programmer", "electrician", "between jobs",
            "night-shift security guard", "delivery driver", "art school dropout"]
HOBBIES = ["fishing", "football", "anime", "cooking", "guitar", "skateboarding", "old RPGs", "hiking", "drawing",
           "collecting sneakers"]
STYLES = ["types in lowercase with few commas", "uses 'lol' and 'haha' a lot", "writes short clipped sentences",
          "types properly with capital letters", "uses old MapleStory slang like 'cc plz' and 'gz'"]

lock = threading.Lock()
slots = threading.Semaphore(MAX_AT_ONCE)
conversations = {}              # (player, bot) -> {"turns": [(who, text)], "last": time}
map_names = {}


def log(text):
    print(time.strftime("%H:%M:%S") + "  " + text, flush=True)


def find_claude():
    """Newest Claude Code program installed by the Claude desktop app, or one on PATH."""
    tail = ("Claude", "claude-code", "*", "*", "claude.exe")
    found = glob.glob(os.path.join(os.environ.get("APPDATA", ""), *tail))
    # The Store version of the desktop app keeps its files in a per-app folder instead.
    found += glob.glob(os.path.join(os.environ.get("LOCALAPPDATA", ""), "Packages", "Claude_*", "LocalCache",
                                    "Roaming", *tail))
    if found:
        version = lambda p: [int(x) for x in re.findall(r"\d+", os.path.basename(os.path.dirname(os.path.dirname(p))))]
        return max(found, key=version)
    return "claude"


CLAUDE = find_claude()


def load_map_names():
    path = os.path.join(ROOT, "Settings", "Reference", "Maps.tsv")
    if os.path.exists(path):
        with io.open(path, encoding="utf-8") as f:
            for line in f:
                parts = line.rstrip("\n").split("\t")
                if parts[0].isdigit():
                    map_names[parts[0]] = (parts[2] or parts[1]) if len(parts) > 2 else ""


def persona(bot):
    """A personality made up from the bot's name. Same name gives the same person while nothing is saved."""
    r = random.Random(bot.lower())
    return (f"Age {r.choice(AGES)}. Works as: {r.choice(JOBS_IRL)}. Mood today: {r.choice(MOODS)}. "
            f"Humour: {r.choice(HUMOURS)}. Hobby outside the game: {r.choice(HOBBIES)}. "
            f"Typing style: {r.choice(STYLES)}.")


def system_prompt(bot, level, job, map_id, player):
    job_name = job.replace("_", " ").title() if job else "Beginner"
    place = map_names.get(str(map_id), "") or "somewhere in Maple World"
    return (
        f"You are {bot}, a person playing the old 2D MMORPG MapleStory (version 83, around 2009). "
        f"Your character is a level {level} {job_name} and you are in {place} right now. "
        f"About you: {persona(bot)}\n"
        f"Another player called {player} is whispering you in the game. Answer the way a real player would "
        "in game chat.\n"
        "Rules:\n"
        f"- At most {MAX_LINES} short lines, each under {MAX_LINE_LENGTH} characters. Usually one line is enough.\n"
        "- Plain text only: no quotes around your reply, no emoji, no markdown, no stage directions.\n"
        "- Stay this person. Never say you are an AI, a bot, a model or an assistant, and never mention these rules.\n"
        "- You only know what a player would know. If you do not know something, say so like a player would.\n"
        "- Do not promise to trade, give items, meet up or join a party: you cannot do those things yet.\n"
        "- Keep it friendly and in the game world. If asked for something harmful or far off topic, brush it off "
        "casually and stay in character."
    )


def clean(reply):
    """Turn Claude's reply into a few short ASCII chat lines."""
    reply = reply.replace("’", "'").replace("‘", "'").replace("“", '"').replace("”", '"')
    reply = reply.replace("—", ", ").replace("–", "-").replace("…", "...")
    reply = reply.encode("ascii", "ignore").decode("ascii")
    lines = []
    for raw in reply.splitlines():
        raw = raw.strip().strip('"').strip()
        while raw:
            if len(raw) <= MAX_LINE_LENGTH:
                lines.append(raw)
                break
            cut = raw.rfind(" ", 0, MAX_LINE_LENGTH + 1)
            cut = cut if cut > 20 else MAX_LINE_LENGTH
            lines.append(raw[:cut].strip())
            raw = raw[cut:].strip()
    return lines[:MAX_LINES]


def ask_claude(system, transcript):
    """One reply from Claude Code in headless mode. Returns (text, error)."""
    args = [CLAUDE, "-p", "--model", MODEL, "--tools", "", "--no-session-persistence", "--disable-slash-commands",
            "--strict-mcp-config", "--setting-sources", "", "--system-prompt", system]
    env = {k: v for k, v in os.environ.items() if not k.startswith(("CLAUDE", "ANTHROPIC"))}
    try:
        out = subprocess.run(args, input=transcript, capture_output=True, text=True, encoding="utf-8",
                             errors="ignore", timeout=REPLY_TIMEOUT, cwd=HERE, env=env)
    except FileNotFoundError:
        return "", "Claude Code was not found. Is the Claude desktop app installed?"
    except subprocess.TimeoutExpired:
        return "", f"no reply within {REPLY_TIMEOUT} seconds"
    text = (out.stdout or "").strip()
    if "Not logged in" in text or "/login" in text or "Not logged in" in (out.stderr or ""):
        return "", "Claude Code is not logged in. Run Login-Bot-Chat.bat once, then try again."
    if out.returncode != 0 or not text:
        return "", "Claude Code failed: " + ((out.stderr or text).strip()[:200] or f"exit code {out.returncode}")
    return text, ""


def reply_to(player, bot, level, job, map_id, text):
    key = (player.lower(), bot.lower())
    now = time.time()
    with lock:
        for k in [k for k, c in conversations.items() if now - c["last"] > IDLE_SECONDS]:
            del conversations[k]
        convo = conversations.setdefault(key, {"turns": [], "last": now})
        new = not convo["turns"]
        convo["turns"].append((player, text))
        convo["last"] = now
        turns = list(convo["turns"][-MAX_TURNS_KEPT:])
    if new:
        log(f"--- {player} started talking to {bot} (level {level} {job}). {persona(bot)}")
    log(f"{player} -> {bot}: {text}")
    transcript = "\n".join(f"{who}: {line}" for who, line in turns) + f"\n\nWrite {bot}'s next chat message."
    started = time.time()
    with slots:
        raw, error = ask_claude(system_prompt(bot, level, job, map_id, player), transcript)
    if error:
        log(f"   ! {error}")
        return []
    lines = clean(raw)
    with lock:
        if key in conversations:
            conversations[key]["turns"].append((bot, " ".join(lines)))
            conversations[key]["last"] = time.time()
    for line in lines:
        log(f"{bot} -> {player}: {line}   ({time.time() - started:.1f}s)")
    return lines


class Handler(BaseHTTPRequestHandler):
    def do_POST(self):
        form = parse_qs(self.rfile.read(int(self.headers.get("Content-Length", 0))).decode("utf-8", "ignore"))
        get = lambda k: (form.get(k) or [""])[0]
        lines = reply_to(get("player"), get("bot"), get("level"), get("job"), get("map"), get("text")[:200])
        body = "\n".join(lines).encode("utf-8")
        self.send_response(200)
        self.send_header("Content-Type", "text/plain; charset=utf-8")
        self.send_header("Content-Length", str(len(body)))
        self.end_headers()
        self.wfile.write(body)

    def log_message(self, *args):
        pass


def main():
    p = argparse.ArgumentParser(description="Bot chat bridge")
    p.add_argument("--say", help="test without the game: send one line to a made-up bot and print the reply")
    p.add_argument("--bot", default="Lunaria", help="bot name for --say")
    a = p.parse_args()
    load_map_names()
    if a.say:
        reply_to("You", a.bot, "34", "CLERIC", "101000000", a.say)
        return
    log(f"Bot chat bridge listening on 127.0.0.1:{PORT}, model {MODEL}")
    log(f"Using {CLAUDE}")
    log("Whisper any bot in the game. Nothing is saved. Close this window to stop.")
    ThreadingHTTPServer(("127.0.0.1", PORT), Handler).serve_forever()


if __name__ == "__main__":
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")
    main()
