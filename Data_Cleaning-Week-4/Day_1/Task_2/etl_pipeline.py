import urllib.request
import json
import pandas as pd
import mysql.connector
from dotenv import load_dotenv
import os

load_dotenv()

api_url = "https://jsonplaceholder.typicode.com/posts"

# extract data from api
try:
    response = urllib.request.urlopen(api_url)
    data = response.read()
    posts = json.loads(data)
    print("\nData fetched from API")
except Exception as e:
    print("\nError fetching data form API: ", e)
    exit()

# load all posts into dataframe
df = pd.DataFrame(posts)

print("\nOrigignal Data:")
print(df.head())

# keep only required columns
df = df[["userId", "id", "title", "body"]]

# validate userId
invalid_userids = df[~df["userId"].apply(lambda x: isinstance(x, int))]

if len(invalid_userids) > 0:
    print("\nInvalid userId rows found!")
    print(invalid_userids)
else:
    print("\nAll userId values are integers.")

# add word count column
df["word_count"] = df["title"].str.split().str.len()

# filter posts word_count>=4
before_filter = len(df)

df = df[df["word_count"] >= 4]

after_filter = len(df)

# cleaning
df["title"] = df["title"].str.title()

# strip
df["body"] = df["body"].str.strip()

# save to csv
df.to_csv("clean_posts.csv", index=False)
print("\n clean_posts.csv file saved.")

# mysql connection
try:
    conn = mysql.connector.connect(
        host='localhost',
        user='root',
        password=os.getenv("password")
    )

    cursor = conn.cursor()

    # drop database
    cursor.execute("DROP DATABASE IF EXISTS posts_db")

    # create database
    cursor.execute("CREATE DATABASE IF NOT EXISTS posts_db")
    print("\nDatabase created successfully!")

    cursor.execute("USE posts_db")

    # create table
    create_table_query="""
    CREATE TABLE IF NOT EXISTS posts(
        userId INT,
        id INT PRIMARY KEY,
        title TEXT,
        body TEXT,
        word_count INT
    )
    """

    cursor.execute(create_table_query)
    print("\nTable created successful")

    # insert data
    insert_query = """
    INSERT INTO VALUES (userID, id, title, body, word_count) VALUES (%s, %s, %s, %s, %s)
    """

    posts_data = list(df.itertuples(index=False, name=None))

    cursor.executemany(insert_query, posts_data)

    conn.commit()
    print("\nData inserted into MySQL")



except Exception as e:
    print("\nMysql connection failed: ",e)

finally:
    if cursor:
       cursor.close()
    if conn:
        conn.close()


# PRINT STATS
print(f"Total posts fetched: {before_filter}")

print(f"Posts after filter: {after_filter}")

# Top 3 users by post count
top_users = df["userId"].value_counts().head(3)

print("\nTop 3 users by post count:")
print(top_users)

print("\nPipeline completed successfully!")