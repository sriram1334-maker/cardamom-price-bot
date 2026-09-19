import pandas as pd

url = "https://www.indianspices.com/marketing/price/domestic/daily-price.html"

tables = pd.read_html(url)

print(f"Total tables found: {len(tables)}")

for i, table in enumerate(tables):
    print("\n" + "=" * 80)
    print(f"TABLE {i}")
    print("=" * 80)
    print(table.head(15))
    print("\nColumns:")
    print(table.columns)
