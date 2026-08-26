import requests
import os

BOT_TOKEN = os.environ["BOT_TOKEN"]
CHAT_ID = os.environ["CHAT_ID"]

message = """
Hello from Cardamom Bot
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
