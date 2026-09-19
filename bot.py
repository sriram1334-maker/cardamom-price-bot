import requests
import pandas as pd
import os
import traceback
from datetime import date

BOT_TOKEN = os.environ["BOT_TOKEN"]
CHAT_ID = os.environ["CHAT_ID"]

SPICES_URL = "https://www.indianspices.com/marketing/price/domestic/daily-price.html"

try:

    # =====================
    # CARDAMOM AUCTION DATA
    # =====================

    tables = pd.read_html(SPICES_URL)

    if len(tables) == 0:
        raise Exception("No tables found")

    small_table = tables[1]

row1 = small_table.iloc[2]
row2 = small_table.iloc[3]

auction_date = str(row1.iloc[1])

auction1_arrived = float(row1.iloc[4])
auction1_sold = float(row1.iloc[5])
auction1_max = float(row1.iloc[6])
auction1_min = float(row1.iloc[7])
auction1_avg = float(row1.iloc[8])

auction2_arrived = float(row2.iloc[4])
auction2_sold = float(row2.iloc[5])
auction2_max = float(row2.iloc[6])
auction2_min = float(row2.iloc[7])
auction2_avg = float(row2.iloc[8])

avg_price = auction1_avg

print("Auction Row 1")
print(row1.tolist())

print("Auction Row 2")
print(row2.tolist())
# =====================
    # WEATHER
    # =====================

    weather_url = (
        "https://api.open-meteo.com/v1/forecast"
        "?latitude=9.85"
        "&longitude=77.15"
        "&current=temperature_2m,relative_humidity_2m,rain"
        "&daily=temperature_2m_max,temperature_2m_min,precipitation_sum"
        "&forecast_days=5"
        "&timezone=Asia/Kolkata"
    )

    weather = requests.get(weather_url).json()

    current = weather["current"]

    temp = current["temperature_2m"]
    humidity = current["relative_humidity_2m"]
    rain = current["rain"]

    # =====================
    # PRICE HISTORY
    # =====================

    try:

        history_df = pd.read_csv("price_history.csv")

    except:

        history_df = pd.DataFrame(
            columns=["date", "avg_price"]
        )

    today = str(date.today())

    if not history_df.empty:

        history_df["avg_price"] = pd.to_numeric(
            history_df["avg_price"],
            errors="coerce"
        )

    if not (history_df["date"] == today).any():

        history_df.loc[len(history_df)] = [
            today,
            avg_price
        ]

        history_df.to_csv(
            "price_history.csv",
            index=False
        )

    # =====================
    # MESSAGE
    # =====================
 def format_auction(row, centre):

    arrived = float(row.iloc[4])
    sold = float(row.iloc[5])
    max_price = float(row.iloc[6])
    min_price = float(row.iloc[7])
    avg_price_row = float(row.iloc[8])

    return f"""
🏢 {centre}

⚖️ Arrived Qty : {arrived:,.1f} Kg
✅ Sold Qty : {sold:,.1f} Kg

📈 Max Price : ₹{max_price:,.0f}/Kg
📉 Min Price : ₹{min_price:,.0f}/Kg
📊 Avg Price : ₹{avg_price_row:,.0f}/Kg
"""
🌿 CardoEla Daily Intelligence Report

📅 {auction_date}

━━━━━━━━━━━━━━━━

💹 CARDAMOM MARKET

{format_auction(row1, "Auction Centre 1")}

━━━━━━━━━━━━━━━━

{format_auction(row2, "Auction Centre 2")}

━━━━━━━━━━━━━━━━

💰 Market Average Price

₹{avg_price:,.2f}/Kg

━━━━━━━━━━━━━━━━

🌦️ WEATHER

🌡️ Temperature : {temp}°C
💧 Humidity : {humidity}%
☔ Rain : {rain} mm

━━━━━━━━━━━━━━━━

📍 Sources
• Spices Board India
• Open-Meteo
"""
except Exception as e:

    print(traceback.format_exc())

    message = f"""
⚠️ CardoEla Alert

Failed to generate today's report.

Error Type:
{type(e).__name__}

Error:
{str(e)}
"""

telegram_url = (
    f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage"
)

requests.post(
    telegram_url,
    data={
        "chat_id": CHAT_ID,
        "text": message
    }
)

print("Message sent successfully")
