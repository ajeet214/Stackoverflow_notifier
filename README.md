# Stackoverflow_notifier

This project automatically monitors new questions posted on StackOverflow for specific tags (like selenium) and sends iOS notifications via Pushover. The GitHub Actions workflow runs every 5 minutes, ensuring you stay updated in real-time without receiving duplicates or stale alerts.

🚀 Features

⏱ Scheduled Monitoring: GitHub Actions runs the notifier every 5 minutes.

📥 Live Scraping: Scrapes StackOverflow for the latest questions tagged with keywords you define.

🔔 Instant Alerts: Sends push notifications using Pushover API.

🧠 De-duplication: Tracks seen questions using data.json to avoid repeat alerts.

🧹 Daily Cleanup: Automatically removes outdated entries from the data store.
