import requests
2
import os
3
4
BOT_TOKEN = os.environ["BOT_TOKEN"]
5
CHAT_ID = os.environ["CHAT_ID"]
6
7
message = """
8
Hello from Cardamom Bot
9
"""
10
11
url = f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage"
12
13
requests.post(
14
url,
15
data={
16
"chat_id": CHAT_ID,
17
"text": message
18
}
19
)
