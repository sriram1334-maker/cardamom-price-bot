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
    # AUCTION DATA
    # =====================

    tables = pd.read_html(SPICES_URL)

    small_table = tables[1]

    row1 = small_table.iloc[2]
    row2 = small_table.iloc[3]

    auction_date = str(row1.iloc[1])

    avg_price = float(row1.iloc[8])

    # =====================
    # WEATHER
    # =====================

    weather_url = (
        "https://api.open-meteo.com/v1/forecast"
        "?latitude=9.85"
        "&longitude=77.15"
        "&current=temperature_2m,relative_humidity_2m,rain"
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
    # WEEKLY TREND
    # =====================

    history_df["avg_price"] = pd.to_numeric(
        history_df["avg_price"],
        errors="coerce"
    )

    last_7_days = history_df.tail(7)

    weekly_trend = ""

    for _, r in last_7_days.iterrows():

        weekly_trend += (
            f"{r['date']} : ₹{r['avg_price']:,.0f}\n"
        )

    if len(last_7_days) >= 2:

        weekly_gain = (
            last_7_days.iloc[-1]["avg_price"]
            - last_7_days.iloc[0]["avg_price"]
        )

    else:

        weekly_gain = 0

    if weekly_gain > 50:
        sentiment = "📈 Bullish"
    elif weekly_gain < -50:
        sentiment = "📉 Bearish"
    else:
        sentiment = "➡️ Stable"

    # =====================
    # FORMAT AUCTION
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

    # =====================
    # MESSAGE
    # =====================

    message = f"""
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

📊 WEEKLY TREND

{weekly_trend}

Weekly Gain :
₹{weekly_gain:,.0f}

Market Sentiment :
{sentiment}

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

telegram_url = f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage"

requests.post(
    telegram_url,
    data={
        "chat_id": CHAT_ID,
        "text": message
    }
)

print("Message sent successfully")
