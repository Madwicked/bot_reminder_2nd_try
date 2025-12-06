import os
import requests
from flask import Flask

app = Flask(__name__)

# ---- CONFIG ----
TOKEN = os.getenv("BOT_TOKEN")
if not TOKEN:
    raise RuntimeError("BOT_TOKEN не задан")

CHAT_ID = -4993967051

TEXT = (
    "‼️Напоминание‼️\n"
    "‼️Не забудь заполнить тайминги‼️\n\n"
    "📋 Форма для заполнения:\n"
    "💻 Web: <a href='https://docs.google.com/forms/d/e/1FAIpQLSd6_bfaZ796YTEjf8rwmseQ8QZe05ZDQxI4KFHgTsWqoKFcmg/viewform'>ссылка</a>\n"
    "📱 Mobile: <a href='https://docs.google.com/forms/d/e/1FAIpQLSd_4mgsQa3pQi2wzuuOhU7y7XbzL1ruGNnfna4tYWL3AVSEpQ/viewform'>ссылка</a>\n\n"
    "🔍 Просмотр таймингов:\n"
    "<a href='https://docs.google.com/spreadsheets/d/1VM8PoYVnGRnCutLV7nvMJ9U1qT8G5d4Y8M-sMjopmCA/edit'>открыть таблицу</a>"
)

# ---- LOGIC ----
def send_msg():
    r = requests.post(
        f"https://api.telegram.org/bot{TOKEN}/sendMessage",
        data={
            "chat_id": CHAT_ID,
            "text": TEXT,
            "parse_mode": "HTML",
        },
        timeout=10,
    )
    return f"Telegram status: {r.status_code}"

# ---- ROUTES ----
@app.route("/")
def home():
    return "OK"

@app.route("/trigger")
def trigger():
    return send_msg()