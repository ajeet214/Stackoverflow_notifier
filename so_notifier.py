#!/usr/bin/env python3
"""
Push an iOS alert whenever a new Stack Overflow question is posted
with any tag in TAGS.
GitHub Action will run this every 2 minutes.
"""
import os, time, json, pathlib, requests, html
from dotenv import load_dotenv

load_dotenv(override=False)

# --- CONFIGURE ---------------------------------------------------------
TAGS = ["selenium", "web-scraping"]          # ← your tag list
CACHE_FILE = pathlib.Path("last_seen.json")  # persisted by Git
SO_API = "https://api.stackexchange.com/2.3/questions"

PUSHOVER_USER = os.getenv["PUSHOVER_USER"]
PUSHOVER_TOKEN = os.getenv["PUSHOVER_TOKEN"]
STACK_APPS_KEY = os.getenv("STACK_APPS_KEY")  # optional
# ----------------------------------------------------------------------

DAY_SEC = 24 * 60 * 60
NOW = int(time.time())
WINDOW_START = NOW - DAY_SEC


if not PUSHOVER_USER or not PUSHOVER_TOKEN:
    raise RuntimeError("Missing Pushover credentials: check env variables/secrets")


def load_seen() -> dict[int, int]:
    if CACHE_FILE.exists():
        with CACHE_FILE.open() as f:
            return {int(k): v for k, v in json.load(f).items()}
    return {}


def save_seen(seen: dict[int, int]) -> None:
    # Keep only IDs in the last 24 h to stop the file growing forever
    trimmed = {qid: dt for qid, dt in seen.items() if dt >= WINDOW_START}
    CACHE_FILE.write_text(json.dumps(trimmed, separators=(",", ":")))



def fetch_recent():
    params = {
        "order": "desc",
        "sort": "creation",
        "site": "stackoverflow",
        "pagesize": 100,
        "fromdate": WINDOW_START,
        "tagged": ";".join(TAGS)
    }
    if STACK_APPS_KEY:
        params["key"] = STACK_APPS_KEY
    r = requests.get(SO_API, params=params, timeout=10)
    r.raise_for_status()
    return r.json()["items"]


def push(title: str, url: str):
    print(f"Pushing: {title}")
    r = requests.post("https://api.pushover.net/1/messages.json", data={
        "token":   PUSHOVER_TOKEN,
        "user":    PUSHOVER_USER,
        "title":   "StackOverflow: new question",
        "message": title,
        "url":     url
    })
    r.raise_for_status()


def main():
    seen = load_seen()                  # question_id → creation_date
    new_items = []

    for q in fetch_recent():
        qid = q["question_id"]
        if qid not in seen:
            new_items.append(q)         # collect unseen
            seen[qid] = q["creation_date"]

    # push oldest→newest for proper ordering
    for q in reversed(new_items):
        push(html.unescape(q["title"]), q["link"])

    save_seen(seen)
    print(f"Pushed {len(new_items)} new questions.")


if __name__ == "__main__":
    main()
