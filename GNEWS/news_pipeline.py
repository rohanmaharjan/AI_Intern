import requests
import csv
import pandas as pd
import os
from dotenv import load_dotenv
import time

#load environment variables
load_dotenv()

url = os.getenv("BASE_URL")
api_key = os.getenv("API_KEY")

#countries to fetch
countries = {
    "Nepal": "np",
    "India": "in",
    "USA": "us",
    "UK": "gb",
    "Australia": "au"
}

#empty list to store data
all_news = []

#fetch data for each country
for country_name, country_code in countries.items():
    print(f'fetching news for {country_name}')

    params = {
        "country": country_code,
        "lang": "en",
        "max": 10,
        "token": api_key
    }

    response = requests.get(url, params=params)

    if response.status_code == 200:
        news_data = response.json()

        news_articles = news_data.get("articles", [])

        for article in news_articles:
            news_item = {
                "country": country_name,
                "title": article.get("title", "N/A"),
                "description": article.get("description", "N/A"),
                "published_at": article.get("publishedAt", "N/A"),
                "source_name": article.get("source", {}).get("name", "N/A"),
                "url": article.get("url", "N/A")
            }

            all_news.append(news_item)
    else:
        print(f'failed to fetch data for {country_name}')
        print("Status Code: ", response.status_code)

    #prevent api rate limit
    time.sleep(3)



# print("\nTotal headlines fetched: ", len(all_news))

# for item in all_news[:5]:
#     print(item)
        
df = pd.DataFrame(all_news)

#clean column names
df.columns = df.columns.str.lower().str.strip()

#Replace missing values with N/A
df.fillna("N/A", inplace=True)

#save to csv
df.to_csv("news_data.csv", index=False)

# print("\nCSV file created successfully: news_data.csv")
# print("Total rows saved:", len(df))

# Preview first 5 rows
# print("\nPreview of saved data:")
# print(df.head())

