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
TEXT = "Напоминание: не забываем сделать задачу!"

def send_msg():
    try:
        response = requests.get(
            f"https://api.telegram.org/bot{TOKEN}/sendMessage",
            params={"chat_id": CHAT_ID, "text": TEXT}
        )
        if response.status_code == 200:
            print("Сообщение отправлено!")
        else:
            print("Ошибка при отправке:", response.text)
    except Exception as e:
        print("Ошибка при запросе:", e)

# Время отправки (UTC+1/UTC+2)
send_time = "18:00"  # поменяй на свое время

# Планирование (каждый день кроме воскресенья)
for day in ["monday", "tuesday", "wednesday", "thursday", "friday", "saturday"]:
    getattr(schedule.every(), day).at(send_time).do(send_msg)

# ---------- Ping для предотвращения сна Render ----------
def ping_self():
    try:
        port = int(os.environ.get("PORT", 8080))
        requests.get(f"http://localhost:{port}/")
        print("Ping self OK")
    except Exception as e:
        print("Ошибка ping:", e)

schedule.every(10).minutes.do(ping_self)

# ---------- Запуск schedule ----------
def run_schedule():
    print("Бот запущен. Ждем времени отправки...")
    while True:
        schedule.run_pending()
        time.sleep(1)

# ---------- Запуск в потоках ----------
if __name__ == "__main__":
    # Flask сервер
    threading.Thread(target=start_flask).start()
    # Schedule (бот + ping)
    run_schedule()