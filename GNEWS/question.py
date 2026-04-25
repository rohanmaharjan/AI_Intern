import pandas as pd

df = pd.read_csv("news_data.csv")

print("\nCSV loaded successfully for analysis")
print("Total rows in CSV:", len(df))

print("\nPreview fo data:")
print(df.head())