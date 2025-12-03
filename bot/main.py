import os
import requests
from flask import Flask

app = Flask(__name__)

TOKEN = os.getenv("BOT_TOKEN")
if not TOKEN:
    raise ValueError("BOT_TOKEN не задан!")

CHAT_ID = -4993967051

TEXT = (
    "‼️Напоминание‼️\n"
    "‼️Не забудь заполнить тайминги‼️\n\n"
    "📋 Форма для заполнения:\n"
    "💻 Web: <a href='https://docs.google.com/forms/d/e/1FAIpQLSd6_bfaZ796YTEjf8rwmseQ8QZe05ZDQxI4KFHgTsWqoKFcmg/viewform'>ссылка</a>\n"
    "📱 Mobile: <a href='https://docs.google.com/forms/d/e/1FAIpQLSd_4mgsQa3pQi2wzuuOhU7y7XbzL1ruGNnfna4tYWL3AVSEpQ/viewform'>ссылка</a>\n\n"
    "🔍 Просмотр таймингов:\n"
    "<a href='https://docs.google.com/spreadsheets/d/1VM8PoYVnGRnCutLV7nvMJ9U1qT8G5d4Y8M-sMjopmCA/edit?gid=1788470692#gid=1788470692'>открыть таблицу</a>"
)

def send_msg():
    try:
        response = requests.post(
            f"https://api.telegram.org/bot{TOKEN}/sendMessage",
            data={"chat_id": CHAT_ID, "text": TEXT, "parse_mode": "HTML"},
            timeout=10
        )
        return f"OK: {response.status_code}"
    except Exception as e:
        return f"ERROR: {e}"

@app.route("/")
def home():
    return "Bot is running!"

# 🔥 endpoint для cron
@app.route("/trigger")
def trigger():
    return send_msg()

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 10000))
    app.run(host="0.0.0.0", port=port)
