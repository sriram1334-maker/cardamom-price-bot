import requests
import pandas as pd
import os

BOT_TOKEN = os.environ["BOT_TOKEN"]
CHAT_ID = os.environ["CHAT_ID"]

URL = "https://www.indianspices.com/marketing/price/domestic/daily-price.html"

try:
    tables = pd.read_html(URL)

    table = tables[1]

    row1 = table.iloc[2]
    row2 = table.iloc[3]

    message = f"""
🌿 CardoEla Daily Auction Report

📅 {row1[3]}

🏢 {row1[1]}
📦 Arrived Qty: {row1[4]} Kg
✅ Sold Qty: {row1[5]} Kg
💰 Avg Price: ₹{row1[8]}/Kg
🚀 Max Price: ₹{row1[6]}/Kg

━━━━━━━━━━━━━━

🏢 {row2[1]}
📦 Arrived Qty: {row2[4]} Kg
✅ Sold Qty: {row2[5]} Kg
💰 Avg Price: ₹{row2[8]}/Kg
🚀 Max Price: ₹{row2[6]}/Kg

📍 Source: Spices Board India
"""

except Exception as e:

    message = f"""
⚠️ CardoEla Alert

Failed to fetch today's cardamom prices.

Error:
{str(e)}

📍 Source: Spices Board India
"""

telegram_url = f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage"

response = requests.post(
    telegram_url,
    data={
        "chat_id": CHAT_ID,
        "text": message
    }
)

print(response.text)
