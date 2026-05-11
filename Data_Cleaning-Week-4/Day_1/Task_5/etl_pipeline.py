from urllib import request,parse
import json
import csv
import mysql.connector
from mysql.connector import Error
import os
from dotenv import load_dotenv
import pandas as pd

# load environment variables
load_dotenv()

base_url = "https://newsapi.org/v2/top-headlines"

# Define parameters
params = {
    "language": "en",   # global headlines in English
    "apiKey": os.getenv("API_KEY")
}

# Encode parameters into URL
url = base_url + "?" + parse.urlencode(params)

def fetch_data(url):
    try:
        response = request.urlopen(url)
        data = response.read().decode()

        news = json.loads(data)
        return news

    except Exception as e:
        print("\nCould not fetch dta from API",e)
        return None

def save_messy_data_to_file(news,filename="messy_news.csv"):
    #convert articles list inot dataframe
    articles = news.get("articles", [])
    df = pd.DataFrame(articles)

    # save to csv
    df.to_csv(filename, index=False)
    print("\nMessy data saved to messy_news.csv")


def main():
    news = fetch_data(url)
    if news:
        save_messy_data_to_file(news)

if __name__ == "__main__":
    main()
    