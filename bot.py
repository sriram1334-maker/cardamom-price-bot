import requests
import pandas as pd
import os
from datetime import date

BOT_TOKEN = os.environ["BOT_TOKEN"]
CHAT_ID = os.environ["CHAT_ID"]

SPICES_URL = "https://www.indianspices.com/marketing/price/domestic/daily-price.html"

try:

    # =====================
    # CARDAMOM AUCTION DATA
    # =====================

    tables = pd.read_html(SPICES_URL)

    table = tables[1]

    row1 = table.iloc[2]
    row2 = table.iloc[3]

    avg_price = float(str(row1[8]).replace(",", ""))

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
    # WEEKLY TREND
    # =====================

    weekly_text = ""
    weekly_gain = 0

    last7 = history_df.tail(7)

    if len(last7) > 1:

        for _, row in last7.iterrows():

            weekly_text += (
                f"{row['date']} : "
                f"₹{row['avg_price']:,.0f}\n"
            )

        weekly_gain = (
            last7.iloc[-1]["avg_price"]
            - last7.iloc[0]["avg_price"]
        )

    # =====================
    # PRICE ALERT
    # =====================

    if avg_price >= 3000:

        price_alert = f"""
✅ Above ₹3,000/kg Target

Current Avg:
₹{avg_price:,.0f}/Kg
"""

    else:

        price_alert = f"""
⚠️ Below ₹3,000/kg Target

Current Avg:
₹{avg_price:,.0f}/Kg
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
    # DISEASE RISK
    # =====================

    if humidity >= 90 and daily_rain >= 10:

        disease_risk = "🔴 HIGH"

        disease_reason = """
• High humidity
• Continuous rainfall
• Increased capsule rot risk
"""

    elif humidity >= 80:

        disease_risk = "🟠 MODERATE"

        disease_reason = """
• Elevated humidity
• Monitor plantation regularly
"""

    else:

        disease_risk = "🟢 LOW"

        disease_reason = """
• Weather relatively favourable
"""

    # =====================
    # TOMORROW OUTLOOK
    # =====================

    pred_low = int(avg_price * 0.99)
    pred_high = int(avg_price * 1.02)

    tomorrow_outlook = f"""
Expected Avg Price:

₹{pred_low:,} - ₹{pred_high:,}

Market Sentiment:

{market_outlook}
"""

    # =====================
    # FORECAST
    # =====================

    forecast_text = ""
    rain_alerts = []

    best_spray_day = None
    lowest_rain = 999

    for i in range(1, 5):

        weather_date = daily["time"][i]

        max_t = daily["temperature_2m_max"][i]
        min_t = daily["temperature_2m_min"][i]
        rain_f = daily["precipitation_sum"][i]

        short_date = (
            weather_date[8:10]
            + "-"
            + weather_date[5:7]
        )

        forecast_text += f"""
📅 {short_date}
🌡️ {min_t}°C - {max_t}°C
🌧️ {rain_f} mm

"""

        if rain_f > 0:
            rain_alerts.append(
                f"🌧️ {short_date} ({rain_f} mm)"
            )

        if rain_f < lowest_rain:
            lowest_rain = rain_f
            best_spray_day = short_date

    rain_summary = (
        "\n".join(rain_alerts)
        if rain_alerts
        else "✅ No rainfall expected."
    )

    heavy_rain_days = []

    for i in range(1, 5):

        rainfall = daily["precipitation_sum"][i]

        if rainfall >= 15:

            heavy_rain_days.append(
                daily["time"][i][8:10]
                + "-"
                + daily["time"][i][5:7]
            )

    heavy_rain_text = (
        "\n".join(heavy_rain_days)
        if heavy_rain_days
        else "None"
    )

    # =====================
    # MESSAGE
    # =====================

    message = f"""
🌿 CardoEla Daily Intelligence Report

📅 {row1[3]}

━━━━━━━━━━━━━━━━

💹 CARDAMOM MARKET

🏢 Auction Centre 1
📦 Arrived Qty : {row1[4]} Kg
✅ Sold Qty : {row1[5]} Kg
💰 Avg Price : ₹{row1[8]}/Kg
🚀 Max Price : ₹{row1[6]}/Kg

━━━━━━━━━━━━━━━━

🏢 Auction Centre 2
📦 Arrived Qty : {row2[4]} Kg
✅ Sold Qty : {row2[5]} Kg
💰 Avg Price : ₹{row2[8]}/Kg
🚀 Max Price : ₹{row2[6]}/Kg

━━━━━━━━━━━━━━━━

🌦️ VELLIMALA WEATHER
📍 Udumbanchola, Idukki

🌡️ Current Temp : {temp}°C
💧 Humidity : {humidity}%
☔ Current Rain : {rain} mm

Today's Forecast

🔺 Max : {max_temp}°C
🔻 Min : {min_temp}°C
🌧️ Rain : {daily_rain} mm

━━━━━━━━━━━━━━━━

📆 4-DAY FORECAST

{forecast_text}

━━━━━━━━━━━━━━━━

☔ RAIN ALERTS

{rain_summary}

⚠️ Heavy Rain Expected On:

{heavy_rain_text}

━━━━━━━━━━━━━━━━

🚜 SPRAY ADVISORY

✅ Best Spray Day:

{best_spray_day}

Reason:
• Lowest rainfall forecast
• Better field accessibility
• Suitable field conditions

━━━━━━━━━━━━━━━━

📈 PRICE TREND

{price_trend_text}

Market Outlook:
{market_outlook}

━━━━━━━━━━━━━━━━

🦠 DISEASE RISK

Capsule Rot Risk:
{disease_risk}

Reasons:
{disease_reason}

━━━━━━━━━━━━━━━━

🎯 PRICE ALERT

{price_alert}

━━━━━━━━━━━━━━━━

📊 WEEKLY TREND

{weekly_text}

Weekly Gain:
₹{weekly_gain:,.0f}

━━━━━━━━━━━━━━━━

🔮 TOMORROW OUTLOOK

{tomorrow_outlook}

━━━━━━━━━━━━━━━━

📍 Sources
• Spices Board India
• Open-Meteo Weather
"""

except Exception as e:

    message = f"""
⚠️ CardoEla Alert

Failed to generate today's report.

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
