import requests
import pandas as pd
import os

BOT_TOKEN = os.environ["BOT_TOKEN"]
CHAT_ID = os.environ["CHAT_ID"]

SPICES_URL = "https://www.indianspices.com/marketing/price/domestic/daily-price.html"

try:

    # CARDAMOM AUCTION DATA
    tables = pd.read_html(SPICES_URL)

    table = tables[1]

    row1 = table.iloc[2]
    row2 = table.iloc[3]

    # WEATHER DATA - VELLIMALA, UDUMBANCHOLA
    weather_url = (
        "https://api.open-meteo.com/v1/forecast"
        "?latitude=9.85"
        "&longitude=77.15"
        "&current=temperature_2m,relative_humidity_2m,rain"
        "&daily=temperature_2m_max,temperature_2m_min,precipitation_sum"
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

    # FARMING ADVISORY
    if daily_rain > 15:
        advice = "⚠️ Heavy rainfall expected. Avoid spraying and fertilizer application."
    elif daily_rain > 5:
        advice = "☔ Moderate rainfall expected. Monitor field conditions before spraying."
    else:
        advice = "✅ Suitable weather for spraying, fertilizer application and harvesting."

    # FINAL MESSAGE
    message = f"""
🌿 CardoEla Daily Market Report

📅 {row1[3]}

━━━━━━━━━━━━━━

🏢 Auction Centre 1

📦 Arrived Qty : {row1[4]} Kg
✅ Sold Qty : {row1[5]} Kg

💰 Avg Price : ₹{row1[8]}/Kg
🚀 Max Price : ₹{row1[6]}/Kg

━━━━━━━━━━━━━━

🏢 Auction Centre 2

📦 Arrived Qty : {row2[4]} Kg
✅ Sold Qty : {row2[5]} Kg

💰 Avg Price : ₹{row2[8]}/Kg
🚀 Max Price : ₹{row2[6]}/Kg

━━━━━━━━━━━━━━

🌦️ Vellimala Weather
📍 Udumbanchola, Idukki

🌡️ Current Temp : {temp}°C
🔺 Max Temp : {max_temp}°C
🔻 Min Temp : {min_temp}°C

💧 Humidity : {humidity}%
☔ Current Rain : {rain} mm
🌧️ Daily Rain : {daily_rain} mm

━━━━━━━━━━━━━━

🚜 Cardamom Advisory

{advice}

━━━━━━━━━━━━━━

📍 Source:
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

response = requests.post(
    telegram_url,
    data={
        "chat_id": CHAT_ID,
        "text": message
    }
)

print(response.text)
