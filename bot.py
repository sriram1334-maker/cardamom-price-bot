import requests
import pandas as pd
import os

BOT_TOKEN = os.environ["BOT_TOKEN"]
CHAT_ID = os.environ["CHAT_ID"]

SPICES_URL = "https://www.indianspices.com/marketing/price/domestic/daily-price.html"

try:

    # CARDAMOM AUCTION
    tables = pd.read_html(SPICES_URL)
    table = tables[1]

    row1 = table.iloc[2]
    row2 = table.iloc[3]

    avg_price = float(str(row1[8]).replace(",", ""))

    # WEATHER - VELLIMALA
    weather_url = (
        "https://api.open-meteo.com/v1/forecast"
        "?latitude=9.85"
        "&longitude=77.15"
        "&current=temperature_2m,relative_humidity_2m,rain"
        "&daily=temperature_2m_max,temperature_2m_min,"
        "precipitation_sum,sunrise,sunset"
        "&forecast_days=5"
        "&timezone=Asia/Kolkata"
    )

    weather = requests.get(weather_url).json()

    current = weather["current"]
    daily = weather["daily"]

    temp = current["temperature_2m"]
    humidity = current["relative_humidity_2m"]
    rain = current["rain"]

    sunrise = daily["sunrise"][0].split("T")[1]
    sunset = daily["sunset"][0].split("T")[1]

    # DISEASE RISK
    if humidity >= 90:
        disease_risk = "🔴 HIGH"
    elif humidity >= 75:
        disease_risk = "🟠 MODERATE"
    else:
        disease_risk = "🟢 LOW"

    # FARM ADVISORY
    today_rain = daily["precipitation_sum"][0]

    if today_rain > 15:
        advice = "⚠️ Avoid spraying and fertilizer application."
    elif today_rain > 5:
        advice = "☔ Monitor rainfall before field operations."
    else:
        advice = "✅ Suitable for spraying and plantation work."

    # FORECAST
    forecast_text = ""
    rain_days = []

    for i in range(1, 5):

        date = daily["time"][i]
        max_t = daily["temperature_2m_max"][i]
        min_t = daily["temperature_2m_min"][i]
        rainfall = daily["precipitation_sum"][i]

        forecast_text += (
            f"\n📅 {date}"
            f"\n🌡️ {min_t}°C - {max_t}°C"
            f"\n🌧️ {rainfall} mm\n"
        )

        if rainfall > 0:
            rain_days.append(
                f"🌧️ {date} ({rainfall} mm)"
            )

    if rain_days:
        rain_summary = "\n".join(rain_days)
    else:
        rain_summary = "✅ No rainfall expected."

    # PRICE ALERT
    if avg_price >= 3000:
        price_alert = f"""
🎯 PRICE ALERT

✅ Above ₹3000 Target

Current Average:
₹{avg_price:,.0f}/Kg
"""
    else:
        price_alert = f"""
🎯 PRICE ALERT

Current Average:
₹{avg_price:,.0f}/Kg
"""

    # FINAL MESSAGE
    message = f"""
🌿 CardoEla Daily Intelligence Report

📅 {row1[3]}

━━━━━━━━━━━━━━

💹 CARDAMOM MARKET

🏢 Auction Centre 1
📦 Arrived : {row1[4]} Kg
✅ Sold : {row1[5]} Kg
💰 Avg : ₹{row1[8]}/Kg
🚀 Max : ₹{row1[6]}/Kg

━━━━━━━━━━━━━━

🏢 Auction Centre 2
📦 Arrived : {row2[4]} Kg
✅ Sold : {row2[5]} Kg
💰 Avg : ₹{row2[8]}/Kg
🚀 Max : ₹{row2[6]}/Kg

━━━━━━━━━━━━━━

🌦️ VELLIMALA WEATHER
📍 Udumbanchola, Idukki

🌡️ Temperature : {temp}°C
💧 Humidity : {humidity}%
☔ Current Rain : {rain} mm

🌅 Sunrise : {sunrise}
🌇 Sunset : {sunset}

━━━━━━━━━━━━━━

🚜 FARM ADVISORY

{advice}

━━━━━━━━━━━━━━

🦠 DISEASE RISK

Capsule Rot Risk:
{disease_risk}

━━━━━━━━━━━━━━

📆 NEXT 4 DAYS

{forecast_text}

━━━━━━━━━━━━━━

☔ RAIN EXPECTED ON

{rain_summary}

━━━━━━━━━━━━━━

{price_alert}

━━━━━━━━━━━━━━

📍 Sources
• Spices Board India
• Open-Meteo
"""

except Exception as e:

    message = f"""
⚠️ CardoEla Alert

Failed to generate report

{str(e)}
"""

requests.post(
    f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage",
    data={
        "chat_id": CHAT_ID,
        "text": message
    }
)
