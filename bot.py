import requests
import pandas as pd
import os

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

    # =====================
    # WEATHER DATA
    # VELLIMALA
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
    # 4 DAY FORECAST
    # =====================

    forecast_text = ""
    rain_alerts = []

    best_spray_day = None
    lowest_rain = 999

    for i in range(1, 5):

        date = daily["time"][i]

        max_t = daily["temperature_2m_max"][i]
        min_t = daily["temperature_2m_min"][i]
        rain_f = daily["precipitation_sum"][i]

        short_date = date[8:10] + "-" + date[5:7]

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

    if rain_alerts:
        rain_summary = "\n".join(rain_alerts)
    else:
        rain_summary = "✅ No rainfall expected."

    heavy_rain_days = []

    for i in range(1, 5):

        rainfall = daily["precipitation_sum"][i]

        if rainfall >= 15:

            heavy_rain_days.append(
                daily["time"][i][8:10]
                + "-"
                + daily["time"][i][5:7]
            )

    if heavy_rain_days:
        heavy_rain_text = "\n".join(heavy_rain_days)
    else:
        heavy_rain_text = "None"

    # =====================
    # FINAL MESSAGE
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
