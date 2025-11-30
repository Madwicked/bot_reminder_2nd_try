import os
import time
import threading
import requests
import schedule
from flask import Flask

# ---------- Flask server для Render ----------
app = Flask(__name__)

@app.route("/")
def home():
    return "Bot is running!"

def start_flask():
    port = int(os.environ.get("PORT", 10000))
    app.run(host="0.0.0.0", port=port)

# ---------- Telegram Bot ----------
TOKEN = os.getenv("BOT_TOKEN")
if not TOKEN:
    raise ValueError("BOT_TOKEN не задан! Проверь переменные окружения на Render.")

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
            data={"chat_id": CHAT_ID, "text": TEXT, "parse_mode": "HTML"}
        )
        if response.status_code == 200:
            print("Сообщение отправлено!")
        else:
            print("Ошибка при отправке:", response.text)
    except Exception as e:
        print("Ошибка при запросе:", e)

# Время (UTC!)
send_time = "05:32"  # УСТАНОВИ СВОЁ ВРЕМЯ В UTC!

# планирование
for day in ["monday", "tuesday", "wednesday", "thursday", "friday", "saturday", "sunday"]:
    getattr(schedule.every(), day).at(send_time).do(send_msg)

# ---------- Ping для предотвращения сна Render ----------
def ping_self():
    try:
        requests.get("https://bot-reminder-2nd-try.onrender.com")
        print("Ping self OK")
    except Exception as e:
        print("Ошибка ping:", e)

schedule.every(5).minutes.do(ping_self)

# ---------- Schedule loop ----------
def run_schedule():
    print("Schedule loop started")
    while True:
        schedule.run_pending()
        time.sleep(1)

# ---------- Запуск ----------
if __name__ == "__main__":
    threading.Thread(target=start_flask).start()
    run_schedule()