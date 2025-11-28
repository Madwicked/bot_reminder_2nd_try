import os
import time
import threading
import requests
import schedule
from flask import Flask

app = Flask(__name__)

@app.route("/")
def home():
    return "Bot is running!"

# --- Telegram ---
TOKEN = os.getenv("BOT_TOKEN")
CHAT_ID = -4993967051
TEXT = (
    "‼️Напоминание‼️\n"
    "‼️Не забудь заполнить тайминги‼️\n\n"
    "📋 Форма для заполнения:\n"
    "Web: https://docs.google.com/forms/d/e/1FAIpQLSd6_bfaZ796YTEjf8rwmseQ8QZe05ZDQxI4KFHgTsWqoKFcmg/viewform\n"
    "Mobile: https://docs.google.com/forms/d/e/1FAIpQLSd_4mgsQa3pQi2wzuuOhU7y7XbzL1ruGNnfna4tYWL3AVSEpQ/viewform\n\n"
    "🔍 Просмотр таймингов:\n"
    "https://docs.google.com/spreadsheets/d/1VM8PoYVnGRnCutLV7nvMJ9U1qT8G5d4Y8M-sMjopmCA/edit?gid=1788470692#gid=1788470692"
)

def send_msg():
    try:
        r = requests.get(
            f"https://api.telegram.org/bot{TOKEN}/sendMessage",
            params={"chat_id": CHAT_ID, "text": TEXT, "parse_mode": "HTML"}
        )
        print("Ответ Telegram:", r.text)
    except Exception as e:
        print("Ошибка отправки:", e)

# --- Планирование ---
send_time = "20:40"  # пример
for day in ["monday", "tuesday", "wednesday", "thursday", "friday", "saturday"]:
    getattr(schedule.every(), day).at(send_time).do(send_msg)

# --- Ping сам себя ---
def ping_self():
    port = int(os.environ.get("PORT", 8080))
    try:
        requests.get(f"http://localhost:{port}/")
        print("Ping OK")
    except Exception as e:
        print("Ping ошибка:", e)

schedule.every(10).minutes.do(ping_self)

# --- Запуск ---
def run_schedule():
    while True:
        schedule.run_pending()
        time.sleep(1)

if __name__ == "__main__":
    threading.Thread(target=lambda: app.run(host="0.0.0.0", port=int(os.environ.get("PORT", 8080)))).start()
    run_schedule()