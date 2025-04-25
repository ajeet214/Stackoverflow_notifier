#!/usr/bin/env python3
"""
Push an iOS alert whenever a new StackOverflow question is posted
with any tag in TAGS.
GitHub Action will run this every 5 minutes.
"""
import json
from datetime import datetime, timedelta
from pathlib import Path
import os, time, requests
from datetime import date
from dotenv import load_dotenv
from so_question_scraper import scrape_questions

load_dotenv(override=False)

# --- CONFIGURE ---------------------------------------------------------
TAGS = ["selenium"]          # ← your tag list
DATA_FILE = Path("data.json")
# persisted by Git
SO_API = "https://api.stackexchange.com/2.3/questions"

PUSHOVER_USER = os.getenv("PUSHOVER_USER")
PUSHOVER_TOKEN = os.getenv("PUSHOVER_TOKEN")
STACK_APPS_KEY = os.getenv("STACK_APPS_KEY")  # optional
# ----------------------------------------------------------------------

DAY_SEC = 24 * 60 * 60
NOW = int(time.time())
WINDOW_START = NOW - DAY_SEC
TODAY = str(date.today())

if not PUSHOVER_USER or not PUSHOVER_TOKEN:
    raise RuntimeError("Missing Pushover credentials: check env variables/secrets")


def is_today_key(data: dict) -> bool:
    try:
        if data[str(date.today())]:
            return True
    except KeyError:
        return False


def add_today_key(data: dict):
    data.setdefault(str(date.today()), [])


def is_seen(question_id: str, data: dict) -> bool:
    print(question_id),
    print(data)

    if not is_today_key(data):
        add_today_key(data)

    if question_id not in data[str(date.today())]:
        return False
    else:
        return True


def save_data(data: dict):
    DATA_FILE.write_text(json.dumps(data, indent=2))


def add_question_id(question_id: str, data: dict) -> dict:

    if question_id not in data[TODAY]:
        data[TODAY].append(question_id)
    return data


def load_data():
    if DATA_FILE.exists():
        return json.loads(DATA_FILE.read_text())
    return {}


def clean_old_entries(data: dict):

    old_key = str(date.today()-timedelta(days=2))
    if old_key in data:
        del data[old_key]
        save_data(data)
    return


def push(title: str, url: str, a_count: str, accepted_answer):
    print(f"Pushing: {title}")
    r = requests.post("https://api.pushover.net/1/messages.json", data={
        "token":   PUSHOVER_TOKEN,
        "user":    PUSHOVER_USER,
        "title":   "StackOverflow: new question",
        "message": title,
        "url":     url,
        "answer_count": a_count,
        "have_accepted": accepted_answer
    })
    r.raise_for_status()


def main(tag_name: str):

    q_list = scrape_questions(tag_name)

    data = load_data()
    for q in q_list:

        question_id = q['question_id']

        if not is_seen(question_id, data):
            print("New question detected! Sending notification...")
            # push notification here
            data = add_question_id(question_id, data)
            save_data(data)
            push(title=q['title'],
                 url=q['question_link'],
                 a_count=q['answer_count'],
                 accepted_answer=q['accepted_answer']
                 )

        else:
            print("Already seen. Skipping...")

    clean_old_entries(data)


if __name__ == "__main__":
    main("selenium")

