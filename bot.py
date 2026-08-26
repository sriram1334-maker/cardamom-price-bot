import requests
import pandas as pd
import os

BOT_TOKEN = os.environ["BOT_TOKEN"]
CHAT_ID = os.environ["CHAT_ID"]

url = "https://www.indianspices.com/marketing/price/domestic/daily-price.html"

tables = pd.read_html(url)

message = "🟢 Spices Board Daily Prices\n\n"

for table in tables:
    if "Cardamom" in table.to_string():
        message += table.head(10).to_string(index=False)
        break

telegram_url = f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage"

requests.post(
    telegram_url,
    data={
        "chat_id": CHAT_ID,
        "text": message[:4000]
    }
)
