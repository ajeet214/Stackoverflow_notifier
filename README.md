# StackOverflow Notifier via GitHub Actions

This project automatically monitors new questions posted on StackOverflow for specific tags (like `selenium`) and sends iOS notifications via [Pushover](https://pushover.net). The GitHub Actions workflow runs every 5 minutes, ensuring you stay updated in real-time without receiving duplicates or stale alerts.

---

## 🚀 Features

- ⏱ **Scheduled Monitoring**: GitHub Actions runs the notifier every 5 minutes.
- 📥 **Live Scraping**: Scrapes StackOverflow for the latest questions tagged with keywords you define.
- 🔔 **Instant Alerts**: Sends push notifications using Pushover API.
- 🧠 **De-duplication**: Tracks seen questions using `data.json` to avoid repeat alerts.
- 🧹 **Daily Cleanup**: Automatically removes outdated entries from the data store.

---

## 📁 Project Structure

```
ajeet214-stackoverflow_notifier/
├── README.md                  # ← You're here
├── __init__.py               # Required for module import
├── data.json                 # Persistent store for notified question IDs
├── requirements              # Project dependencies
├── sample.py                 # Sample test for Pushover setup
├── so_notifier.py            # Core script: scraping + notification logic
├── so_question_scraper.py    # StackOverflow HTML scraper
└── .github/
    └── workflows/
        └── notifier.yml      # GitHub Action workflow file
```

---

## 🛠 Setup Instructions

### 1. Clone the Repository
```bash
git clone https://github.com/ajeet214/stackoverflow_notifier.git
cd stackoverflow_notifier
```

### 2. Create `.env` File
Create a `.env` file in the root directory with the following contents:
```env
PUSHOVER_USER=your_pushover_user_key
PUSHOVER_TOKEN=your_pushover_app_token
STACK_APPS_KEY=your_optional_stackapps_key
```

### 3. Install Dependencies
```bash
pip install -r requirements
```

---

## 🧪 Testing Locally
You can test the notification system locally using:
```bash
python sample.py
```
Then, run the main notifier script:
```bash
python so_notifier.py
```

---

## ⚙️ GitHub Actions Workflow

The file `.github/workflows/notifier.yml` runs every 5 minutes using `cron`. It:
- Installs dependencies
- Loads secrets from GitHub
- Runs `so_notifier.py`
- Commits updates to `data.json` to persist question history

Make sure to store your secrets in the GitHub repository settings under **Settings > Secrets and variables > Actions**:
- `PUSHOVER_USER`
- `PUSHOVER_TOKEN`
- `STACK_APPS_KEY` (optional)
- `GHB_TOKEN` (used to push commits)

---

## 📚 Explanation of Key Files

### `so_question_scraper.py`
Scrapes the latest StackOverflow questions using the provided tag. Extracts metadata like question ID, title, tags, and author details.

### `so_notifier.py`
Main orchestrator. Loads past seen question IDs from `data.json`, scrapes new questions, checks if any are unseen and recent, and pushes a notification. Updates the store with new question IDs.

### `data.json`
A dictionary of the format:
```json
{
  "2025-04-25": [32984732, 3249874849, 1237874],
  "2025-04-26": [324984, 432424, 124342]
}
```
Used to avoid sending duplicate alerts.

---

## 📈 Ideas for Future Enhancements

- Support multiple tags in parallel
- Add Slack or Telegram notifications
- Persist data in a lightweight database (e.g., SQLite)
- Filter based on vote/view/answer count

---

## 🙏 Acknowledgments

- [StackExchange API](https://api.stackexchange.com/)
- [BeautifulSoup](https://www.crummy.com/software/BeautifulSoup/)
- [Pushover](https://pushover.net/)

---

## 📄 License
MIT License. See `LICENSE` file (if added).

