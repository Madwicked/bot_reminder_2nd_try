import os
import time
import requests
import schedule
from flask import Flask
import threading

# Telegram
TOKEN = os.getenv("BOT_TOKEN")
CHAT_ID = -4993967051

TEXT = """
<b>Напоминание</b><br>
Заполни тайминги!
"""

app = Flask(__name__)

@app.get("/")
def home():
    return "Bot running!"

def send_msg():
    print("Пытаюсь отправить...")
    try:
        r = requests.get(
            f"https://api.telegram.org/bot{TOKEN}/sendMessage",
            params={"chat_id": CHAT_ID, "text": TEXT, "parse_mode": "HTML"}
        )
        print("Ответ Telegram:", r.text)
    except Exception as e:
        print("Ошибка отправки:", e)

# Расписание
send_time = "19:45"

schedule.every().monday.at(send_time).do(send_msg)
schedule.every().tuesday.at(send_time).do(send_msg)
schedule.every().wednesday.at(send_time).do(send_msg)
schedule.every().thursday.at(send_time).do(send_msg)
schedule.every().friday.at(send_time).do(send_msg)
schedule.every().saturday.at(send_time).do(send_msg)

print("Scheduler initialized")

# ───────────────────────────────────────────────
# ВАЖНО: scheduler_loop запускаем СРАЗУ
# ───────────────────────────────────────────────
def scheduler_loop():
    print("Scheduler loop started")
    while True:
        schedule.run_pending()
        time.sleep(1)

threading.Thread(target=scheduler_loop, daemon=True).start()

# ───────────────────────────────────────────────
# Flask запускаем как обычно
# ───────────────────────────────────────────────
port = int(os.environ.get("PORT", 10000))
app.run(host="0.0.0.0", port=port)