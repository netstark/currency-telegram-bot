import requests
from apscheduler.schedulers.blocking import BlockingScheduler

TOKEN = '8108776548:AAEjeT3UjPasnJVw7q0wVt1ASlQuPO8CoXg'
CHAT_ID = '549415850'

scheduler = BlockingScheduler(timezone='Europe/Kyiv')


def get_currency_rates():
    url = 'https://bank.gov.ua/NBUStatService/v1/statdirectory/exchange?json'
    response = requests.get(url)
    data = response.json()
    usd = next((x for x in data if x['cc'] == 'USD'), None)
    eur = next((x for x in data if x['cc'] == 'EUR'), None)

    if usd and eur:
        return f"\U0001F4B1 Курси валют:\nUSD: {usd['rate']:.2f} грн\nEUR: {eur['rate']:.2f} грн"
    else:
        return "Не вдалося отримати курси."


def send_message():
    text = get_currency_rates()
    url = f"https://api.telegram.org/bot{TOKEN}/sendMessage"
    payload = {"chat_id": CHAT_ID, "text": text}
    requests.post(url, data=payload)


# Щодня о 09:00 за Києвом
scheduler.add_job(send_message, 'cron', hour=9, minute=0)

print("Бот запущено. Надсилаю тестове повідомлення...")
send_message()  # Надіслати одразу
scheduler.start()
