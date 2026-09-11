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
        raise Exception("No tables found on Spices Board website")

    table = None

    for t in tables:
        if len(t) >= 2 and len(t.columns) >= 9:
            table = t
            break

    if table is None:
        raise Exception("Valid auction table not found")

    table = table.dropna(how="all").reset_index(drop=True)

    print(f"Tables Found: {len(tables)}")
    print(f"Rows Found: {len(table)}")

    if len(table) < 2:
        raise Exception(
            f"Auction data not available. Rows found: {len(table)}"
        )

    row1 = table.iloc[0]
    row2 = table.iloc[1]

    auction_date = row1.iloc[3]

    avg_price = float(
        str(row1.iloc[8])
        .replace(",", "")
        .replace("₹", "")
        .strip()
    )

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
    # PRICE TREND
    # =====================

    price_trend_text = "Not enough historical data."
    market_outlook = "🟡 Stable"

    if len(history_df) >= 2:

        today_price = history_df.iloc[-1]["avg_price"]
        yesterday_price = history_df.iloc[-2]["avg_price"]

        change = today_price - yesterday_price

        percent = (
            change / yesterday_price
        ) * 100

        if change > 0:
            market_outlook = "🟢 Bullish"
        elif change < 0:
            market_outlook = "🔴 Bearish"

        price_trend_text = f"""
Yesterday : ₹{yesterday_price:,.0f}/Kg
Today : ₹{today_price:,.0f}/Kg
Change : ₹{change:+,.0f} ({percent:+.2f}%)
"""

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
    daily = weather["daily"]

    temp = current["temperature_2m"]
    humidity = current["relative_humidity_2m"]
    rain = current["rain"]

    max_temp = daily["temperature_2m_max"][0]
    min_temp = daily["temperature_2m_min"][0]
    daily_rain = daily["precipitation_sum"][0]

    # =====================
    # MESSAGE
    # =====================

    message = f"""
🌿 CardoEla Daily Intelligence Report

📅 {auction_date}

━━━━━━━━━━━━━━━━

💹 CARDAMOM MARKET

🏢 Auction Centre 1
📦 Arrived Qty : {row1.iloc[4]}
✅ Sold Qty : {row1.iloc[5]}
💰 Avg Price : ₹{row1.iloc[8]}/Kg
🚀 Max Price : ₹{row1.iloc[6]}/Kg

━━━━━━━━━━━━━━━━

🏢 Auction Centre 2
📦 Arrived Qty : {row2.iloc[4]}
✅ Sold Qty : {row2.iloc[5]}
💰 Avg Price : ₹{row2.iloc[8]}/Kg
🚀 Max Price : ₹{row2.iloc[6]}/Kg

━━━━━━━━━━━━━━━━

🌦️ VELLIMALA WEATHER

🌡️ Current Temp : {temp}°C
💧 Humidity : {humidity}%
☔ Current Rain : {rain} mm

Today's Forecast

🔺 Max : {max_temp}°C
🔻 Min : {min_temp}°C
🌧️ Rain : {daily_rain} mm

━━━━━━━━━━━━━━━━

📈 PRICE TREND

{price_trend_text}

Market Outlook:
{market_outlook}

━━━━━━━━━━━━━━━━

📍 Sources
• Spices Board India
• Open-Meteo Weather
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

# =====================
# TELEGRAM
# =====================

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
