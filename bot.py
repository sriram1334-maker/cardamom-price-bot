import pandas as pd

pd.set_option('display.max_columns', None)
pd.set_option('display.expand_frame_repr', False)
pd.set_option('display.max_colwidth', None)
pd.set_option('display.width', 1000)

url = "https://www.indianspices.com/marketing/price/domestic/daily-price.html"

table = pd.read_html(url)[1]

print(table.to_string(index=False))
