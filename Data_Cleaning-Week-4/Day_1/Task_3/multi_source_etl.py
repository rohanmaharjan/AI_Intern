import urllib.request
import json
import pandas as pd
import mysql.connector
import os
from dotenv import load_dotenv

load_dotenv()

# DATABASE CONFIG
DATABASE_NAME = "etl_db"


# fetch data
def fetch_api_data(url):

    try:
        response = urllib.request.urlopen(url)
        data = response.read()
        json_data = json.loads(data)
        print("Data fetched successfully")

        return json_data

    except Exception as e:
        print(f"Error fetching API data:\n{e}")
        exit


# create database
def create_database():

    try:
        conn = mysql.connector.connect(
            host='localhost',
            user='root',
            password=os.getenv("password")
        )

        cursor = conn.cursor()

        cursor.execute(
            f"CREATE DATABASE IF NOT EXISTS {DATABASE_NAME}"
        )

        print(f"Database '{DATABASE_NAME}' created\n")

        cursor.close()
        conn.close()

    except mysql.connector.Error as e:
        print("Database creation failed", e)


# CONNECT DATABASE
def connect_database():

    try:
        conn = mysql.connector.connect(
            host='localhost',
            user='root',
            password=os.getenv("password"),
            database=DATABASE_NAME
        )

        print("Connected to MySQL successfully\n")

        return conn

    except mysql.connector.Error as e:
        print("MySQL connection failed", e)
        exit

# main program
def main():

    try:

        #create database
        create_database()

        conn = connect_database()

        if conn is None:
            return

        cursor = conn.cursor()

        # urls
        USERS_URL = "https://jsonplaceholder.typicode.com/users"
        POSTS_URL = "https://jsonplaceholder.typicode.com/posts"
        TODOS_URL = "https://jsonplaceholder.typicode.com/todos"

        users_data = fetch_api_data(USERS_URL)
        posts_data = fetch_api_data(POSTS_URL)
        todos_data = fetch_api_data(TODOS_URL)

        # create dataframes
        df_users = pd.json_normalize(users_data)
        df_posts = pd.DataFrame(posts_data)
        df_todos = pd.DataFrame(todos_data)

        print("DataFrames created successfully\n")

        # keep id, name, email, city for user
        df_users = df_users[
            ["id", "name", "email", "address.city"]
        ]

        df_users.rename(
            columns={
                "address.city": "city"
            },
            inplace=True
        )

        # keep userId, title and rename userId -> id for posts
        df_posts = df_posts[
            ["userId", "title"]
        ]

        df_posts.rename(
            columns={
                "userId": "id"
            },
            inplace=True
        )

        # bonus todos
        df_todos = df_todos[
            ["userId", "completed"]
        ]

        df_todos.rename(
            columns={
                "userId": "id"
            },
            inplace=True
        )

        # merge users and posts
        merged_df = pd.merge(
            df_users,
            df_posts,
            on="id"
        )

        print("Users and posts merged successfully\n")

        # count posts per users
        post_count = df_posts.groupby("id").size().reset_index(name="post_count")

        # Add post_count into users dataframe
        df_users = pd.merge(
            df_users,
            post_count,
            on="id",
            how="left"
        )

        # bonus complition rate
        completion_rate = df_todos.groupby("id")["completed"].mean().reset_index(name="completion_rate")

        completion_rate["completion_rate"] = (completion_rate["completion_rate"] * 100).round(2)

        df_users = pd.merge(
            df_users,
            completion_rate,
            on="id",
            how="left"
        )

        # clean data
        df_users["email"] = df_users["email"].str.lower()

        df_users["name"] = df_users["name"].str.strip()

        df_users["city"] = df_users["city"].str.strip()

        df_users.dropna(inplace=True)

        print("Data cleaned successfully\n")

        # save csv
        df_users.to_csv("merged_data.csv",index=False)

        print("CSV file saved as 'merged_data.csv'\n")

        # create table
        create_table_query = """
        CREATE TABLE IF NOT EXISTS merged_users (
            id INT PRIMARY KEY,
            name VARCHAR(255),
            email VARCHAR(255),
            city VARCHAR(255),
            post_count INT,
            completion_rate FLOAT
        )
        """

        cursor.execute(create_table_query)

        print("Table 'merged_users' created\n")

        # insert data
        cursor.execute("DELETE FROM merged_users")

        insert_query = """
        INSERT INTO merged_users
        (
            id,
            name,
            email,
            city,
            post_count,
            completion_rate
        )
        VALUES (%s, %s, %s, %s, %s, %s)
        """

        for _, row in df_users.iterrows():

            values = (
                int(row["id"]),
                row["name"],
                row["email"],
                row["city"],
                int(row["post_count"]),
                float(row["completion_rate"])
            )

            cursor.execute(insert_query, values)

        conn.commit()

        print("Data inserted into MySQL successfully\n")

        # top three active users
        print("TOP 3 MOST ACTIVE USERS\n")

        top_users = df_users.sort_values(by="post_count",ascending=False).head(3)

        for _, row in top_users.iterrows():

            print(f"""
                    ID: {row['id']}
                    Name: {row['name']}
                    Email: {row['email']}
                    City: {row['city']}
                    Post Count: {row['post_count']}
                    Completion Rate: {row['completion_rate']}%
                """)

        # close conenction
        cursor.close()
        conn.close()

        print("ETL PIPELINE COMPLETED SUCCESSFULLY")

    except Exception as e:
        print(f"Unexpected error:\n{e}")

if __name__ == "__main__":
    main()