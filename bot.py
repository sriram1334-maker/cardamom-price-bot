import pandas as pd

url = "https://www.indianspices.com/marketing/price/domestic/daily-price.html"

table = pd.read_html(url)[1]

print(table)
