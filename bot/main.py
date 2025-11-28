import os
import time
import requests
import schedule

# Проверка переменной окружения
TOKEN = os.environ.get("BOT_TOKEN")
CHAT_ID = -4993967051  # Заменить на свой ID группы
TEXT = "Напоминание: не забываем сделать задачу!"

if not TOKEN:
    raise ValueError("BOT_TOKEN не задан! Проверьте Variables на Railway")

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

# Время отправки (UTC)
send_time = "14:00"  # Пример: 14:00 UTC

# Планируем каждый день кроме воскресенья
schedule.every().monday.at(send_time).do(send_msg)
schedule.every().tuesday.at(send_time).do(send_msg)
schedule.every().wednesday.at(send_time).do(send_msg)
schedule.every().thursday.at(send_time).do(send_msg)
schedule.every().friday.at(send_time).do(send_msg)
schedule.every().saturday.at(send_time).do(send_msg)

print("Бот запущен. Ждем времени отправки...")

while True:
    schedule.run_pending()
    time.sleep(1)