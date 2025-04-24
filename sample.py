import os, http.client, urllib
from dotenv import load_dotenv

load_dotenv()

conn = http.client.HTTPSConnection("api.pushover.net:443")
conn.request("POST", "/1/messages.json",
  urllib.parse.urlencode({
    "token": os.getenv("PUSHOVER_TOKEN"),
    "user": os.getenv("PUSHOVER_USER"),
    "message": "this is test message",
  }), { "Content-type": "application/x-www-form-urlencoded" })
conn.getresponse()
