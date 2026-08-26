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
🟢 Cardamom Daily Price Update
9
 
10
6 mm : ₹1800/kg
11
7 mm : ₹2100/kg
12
8 mm : ₹2500/kg
13
"""
14
 
15
url = f"https://api.telegram.org/bot8224279466:AAGAvT1bhik88B6qMdvq4oaOxG8mQsQsK08/sendMessage"
16
 
17
requests.post(
18
url,
19
data={
20
"chat_id": CHAT_ID,
21
"text": message
22
}
23
)
