import requests
import os

BOT_TOKEN = os.environ["BOT_TOKEN"]
CHAT_ID = os.environ["CHAT_ID"]

message ="""
🟢 Cardamom Daily Price Update
6 mm : ₹1800/kg
7 mm : ₹2100/kg
7+ mm : ₹2250/kg
8 mm : ₹2500/kg
8+ mm : ₹2900/kg
Regards,
CardoEla
"""

url = f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage"

requests.post(
    url,
    data={
        "chat_id": CHAT_ID,
        "text": message
    }
)

print("Message sent")
