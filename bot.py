import requests
import pandas as pd
import os

BOT_TOKEN = os.environ["BOT_TOKEN"]
CHAT_ID = os.environ["CHAT_ID"]

URL = "https://www.indianspices.com/marketing/price/domestic/daily-price.html"

tables = pd.read_html(URL)

message = "📋 TABLE STRUCTURE\n\n"

for i, table in enumerate(tables):
    message += f"\nTable {i}\n"
    message += str(table.head())
    message += "\n\n"

telegram_url = f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage"

requests.post(
    telegram_url,
    data={
        "chat_id": CHAT_ID,
        "text": message[:4000]
    }
)

print("Sent")
