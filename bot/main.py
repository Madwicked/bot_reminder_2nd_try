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
    port = int(os.environ.get("PORT", 8080))
    app.run(host="0.0.0.0", port=port)

# ---------- Telegram Bot ----------
TOKEN = os.getenv("BOT_TOKEN")
if not TOKEN:
    raise ValueError("BOT_TOKEN не задан! Проверьте переменные окружения на Render.")

CHAT_ID = -4993967051  # ID группы

# HTML-формат сообщения
TEXT = """
<b>‼️Напоминание‼️</b><br>
<b>‼️Не забудь заполнить тайминги‼️</b><br><br>

📋 <b>Форма для заполнения:</b><br>
💻 Web: <a href="https://docs.google.com/forms/d/e/1FAIpQLSd6_bfaZ796YTEjf8rwmseQ8QZe05ZDQxI4KFHgTsWqoKFcmg/viewform">ссылка</a><br>
📱 Mobile: <a href="https://docs.google.com/forms/d/e/1FAIpQLSd_4mgsQa3pQi2wzuuOhU7y7XbzL1ruGNnfna4tYWL3AVSEpQ/viewform">ссылка</a><br><br>

🔍 <b>Просмотр таймингов:</b><br>
<a href="https://docs.google.com/spreadsheets/d/1VM8PoYVnGRnCutLV7nvMJ9U1qT8G5d4Y8M-sMjopmCA/edit?gid=1788470692#gid=1788470692">открыть таблицу</a>
"""

def send_msg():
    print("Пробую отправить...")
    try:
        response = requests.get(
            f"https://api.telegram.org/bot{TOKEN}/sendMessage",
            params={
                "chat_id": CHAT_ID,
                "text": TEXT,
                "parse_mode": "HTML"
            }
        )
        print("Ответ Telegram:", response.text)

        if response.status_code == 200:
            print("Сообщение отправлено!")
        else:
            print("Ошибка отправки!")
    except Exception as e:
        print("Ошибка:", e)

# Время отправки (UTC+1/UTC+2)
send_time = "20:17"

# Планирование (как у тебя — рабочее!)
for day in ["monday", "tuesday", "wednesday", "thursday", "friday", "saturday"]:
    getattr(schedule.every(), day).at(send_time).do(send_msg)

# ---------- Ping для предотвращения сна Render ----------
def ping_self():
    try:
        port = int(os.environ.get("PORT", 8080))
        requests.get(f"http://localhost:{port}/")
        print("Ping OK")
    except:
        print("Ping error")

schedule.every(10).minutes.do(ping_self)

# Запуск schedule
def run_schedule():
    print("Бот запущен. Ждём отправки...")
    while True:
        schedule.run_pending()
        time.sleep(1)

# ---------- Запуск ----------
if __name__ == "__main__":
    threading.Thread(target=start_flask).start()
    run_schedule()