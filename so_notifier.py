#!/usr/bin/env python3
"""
Push an iOS alert whenever a new Stack Overflow question is posted
with any tag in TAGS.
GitHub Action will run this every 2 minutes.
"""
import os, time, json, pathlib, requests, html

# --- CONFIGURE ---------------------------------------------------------
TAGS = ["selenium", "web-scraping"]          # ← your tag list
CACHE_FILE = pathlib.Path("last_seen.json")  # persisted by Git
SO_API = "https://api.stackexchange.com/2.3/questions"
PUSHOVER_USER = os.environ["PUSHOVER_USER"]
PUSHOVER_TOKEN = os.environ["PUSHOVER_TOKEN"]
STACK_APPS_KEY = os.getenv("STACK_APPS_KEY")  # optional
# ----------------------------------------------------------------------


def load_cache() -> dict:
    if CACHE_FILE.exists():
        return json.loads(CACHE_FILE.read_text())
    return {"last": 0}


def save_cache(data: dict) -> None:
    CACHE_FILE.write_text(json.dumps(data))

def fetch_new(since: int):
    params = {
        "order": "desc",
        "sort":  "creation",
        "site":  "stackoverflow",
        "pagesize": 30,
        "fromdate": since + 1,
        "tagged":  ";".join(TAGS)
    }
    if STACK_APPS_KEY:
        params["key"] = STACK_APPS_KEY
    r = requests.get(SO_API, params=params, timeout=10)
    r.raise_for_status()
    return r.json()["items"]


def push(title: str, url: str):
    r = requests.post("https://api.pushover.net/1/messages.json", data={
        "token":   PUSHOVER_TOKEN,
        "user":    PUSHOVER_USER,
        "title":   "StackOverflow: new question",
        "message": title,
        "url":     url
    })
    r.raise_for_status()


def main():
    cache = load_cache()
    for q in reversed(fetch_new(cache["last"])):
        push(html.unescape(q["title"]), q["link"])
        cache["last"] = max(cache["last"], q["creation_date"])
    save_cache(cache)


if __name__ == "__main__":
    main()
