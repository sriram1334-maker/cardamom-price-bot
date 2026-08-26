import requests
import pandas as pd
import os

BOT_TOKEN = os.environ["BOT_TOKEN"]
CHAT_ID = os.environ["CHAT_ID"]

URL = "https://www.indianspices.com/marketing/price/domestic/daily-price.html"

try:
    tables = pd.read_html(URL)

    auction_table = None

    for table in tables:
        if "Auctioneer" in table.to_string():
            auction_table = table
            break

    if auction_table is not None and len(auction_table) > 0:

        row = auction_table.iloc[0]

        auctioneer = str(row.iloc[0])
        auction_date = str(row.iloc[3])
        arrived_qty = str(row.iloc[4])
        sold_qty = str(row.iloc[5])
        max_price = str(row.iloc[6])
        min_price = str(row.iloc[7])
        avg_price = str(row.iloc[8])

        message = f"""
<b>🌿 CardoEla Daily Auction Report</b>

📅 <b>{auction_date}</b>

🏢 <b>{auctioneer}</b>

📦 Arrived Qty: <b>{arrived_qty} Kg</b>
✅ Sold Qty: <b>{sold_qty} Kg</b>

💰 Avg Price: <b>₹{avg_price}/Kg</b>
⬇️ Min Price: <b>₹{min_price}/Kg</b>
🚀 Max Price: <b>₹{max_price}/Kg</b>

📍 <i>Source: Spices Board India</i>
"""

    else:
        message = """
⚠️ CardoEla Alert

Unable to find cardamom auction data today.

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

requests.post(
    telegram_url,
    data={
        "chat_id": CHAT_ID,
        "text": message,
        "parse_mode": "HTML"
    }
)

print("Message sent successfully")
