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

    auction_rows = []

    for tbl in tables:

        tbl = tbl.dropna(how="all").reset_index(drop=True)

        for i in range(len(tbl)):

            row = tbl.iloc[i]

            for col in range(len(row)):

                try:

                    value = str(row.iloc[col])

                    value = value.replace(",", "").replace("₹", "").strip()

                    price = float(value)

                    if price > 500:
                        auction_rows.append(row)
                        break

                except:
                    pass

            if len(auction_rows) >= 2:
                break

        if len(auction_rows) >= 2:
            break

    if len(auction_rows) < 2:
        raise Exception(
            "Could not find auction rows in Spices Board table"
        )

    row1 = auction_rows[0]
    row2 = auction_rows[1]

    print("Auction Row 1")
    print(row1)

    print("Auction Row 2")
    print(row2)

    # Adjust if website structure changes
    avg_price = None

    for value in row1:

        try:

            temp = str(value).replace(",", "").replace("₹", "").strip()

            number = float(temp)

            if number > 500:
                avg_price = number
                break

        except:
            continue

    if avg_price is None:
        raise Exception("Average price not found")

    auction_date = str(date.today())

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

    message = f"""
🌿 CardoEla Daily Intelligence Report

📅 {auction_date}

━━━━━━━━━━━━━━━━

💹 CARDAMOM MARKET

🏢 Auction Centre 1

{row1.to_string()}

━━━━━━━━━━━━━━━━

🏢 Auction Centre 2

{row2.to_string()}

━━━━━━━━━━━━━━━━

💰 Average Price

₹{avg_price:,.0f}/Kg

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
