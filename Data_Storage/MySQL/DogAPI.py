'''
Goal Build a complete automated data system — fetch, store, analyse, and export. No manual steps.
Fetch API
requests
→
Error handle
try/except
→
Store MySQL
mysql.connector
→
Analyse
SQL queries
→
Export
CSV + TXT
Must Fetch data from any public API with error handling
Must Store ALL fetched data in a properly structured MySQL database
Must Run at least 3 meaningful SQL queries and print results with labels
Must Export query results to a CSV file (combine Week 1 + Week 3)
Must Handle errors at every step — API, database, file
Should Write reusable functions: fetch_data(), store_data(), run_report()
Bonus Schedule it: run the whole thing every time you run the script fres
'''
import requests
import mysql.connector
from dotenv import load_dotenv
import os
import pandas as pd

load_dotenv()

def connect_database():
    conn = mysql.connector.connect(
            host="localhost",
            user="root",
            password=os.getenv("Database_Password"),
            database="dog_db"
        )
    cursor = conn.cursor()
    return conn,cursor

#create database
def create_database():
    try:
        conn = mysql.connector.connect(
            host="localhost",
            user="root",
            password=os.getenv("Database_Password")
        )

        cursor = conn.cursor()

        cursor.execute("CREATE DATABASE IF NOT EXISTS dog_db")
        print("\nDAtabase created successfully")

        cursor.close()
        conn.close()
    except mysql.connector.Error as e:
        print("Databse Error:", e)

#Create table function
def create_table():
    try:
        conn, cursor = connect_database()
        cursor.execute("""
        CREATE TABLE IF NOT EXISTS dogs (
            id INT PRIMARY KEY,
            name VARCHAR(100),
            life_span VARCHAR(100),
            temperament TEXT,
            origin VARCHAR(100),
            breed_group VARCHAR(100),
            weight VARCHAR(50),
            height VARCHAR(50)
        )
        """)

        print("Table 'dogs' created successfully.")

        cursor.close()
        conn.close()

    except mysql.connector.Error as err:
        print("Table Error:", err)

# fetch data from API
def fetch_data():
    url = "https://api.thedogapi.com/v1/breeds"

    params = {
        "api_key": os.getenv("API_KEY")
    }

    try:
        response = requests.get(url, params=params, timeout=10)

        response.raise_for_status()

        dog_data = response.json()

        print(f'fetched {len(dog_data)} dog breeds successfully')
        return dog_data
    
    except requests.exceptions.Timeout:
        print("error: request timeout")
        return []
    
    except requests.exceptions.ConnectionError:
        print("Error: Connection problem.")
        return []

    except requests.exceptions.HTTPError as err:
        print("HTTP Error:", err)
        return []

    except Exception as e:
        print("Unexpected Error:", e)
        return []

# store dog data
def store_data(dog_data):
    try:
        conn, cursor = connect_database()
        # insert ignore used to avoid duplication while running script again
        insert_query = """
        INSERT IGNORE INTO dogs
        (id, name, life_span, temperament, origin, breed_group, weight, height)
        VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
        """

        for dog in dog_data:
            dog_id = dog.get("id")
            name = dog.get("name")
            life_span = dog.get("life_span")
            temperament = dog.get("temperament")
            origin = dog.get("origin")
            breed_group = dog.get("breed_group")

            # nested JSON fields
            weight = dog.get("weight", {}).get("metric")
            height = dog.get("height", {}).get("metric")

            values = (
                dog_id,
                name,
                life_span,
                temperament,
                origin,
                breed_group,
                weight,
                height
            )

            cursor.execute(insert_query, values)

        conn.commit()

        print("Data stored successfully in MySQL.")

        cursor.close()
        conn.close()

    except mysql.connector.Error as err:
        print("Store Data Error:", err)

# analyze data
def run_report():
    try:
        conn, cursor = connect_database()

        # Query 1: Dogs with longest lifespan
        print("\nQuery 1: Top 10 Dogs with Longest Lifespan")

        query1 = """
        SELECT name, life_span
        FROM dogs
        WHERE life_span IS NOT NULL
        LIMIT 10
        """

        cursor.execute(query1)

        result1 = cursor.fetchall()

        for row in result1:
            print(row)

        # Query 2: Count by breed group
        print("\nQuery 2: Count of Dogs by Breed Group")

        query2 = """
        SELECT breed_group, COUNT(*)
        FROM dogs
        WHERE breed_group IS NOT NULL
        GROUP BY breed_group
        ORDER BY COUNT(*) DESC
        """

        cursor.execute(query2)

        result2 = cursor.fetchall()

        for row in result2:
            print(row)

        # Query 3: Dogs with known origin
        print("\nQuery 3: Dogs with Known Origin")

        query3 = """
        SELECT name, origin
        FROM dogs
        WHERE origin IS NOT NULL
        LIMIT 10
        """

        cursor.execute(query3)

        result3 = cursor.fetchall()

        for row in result3:
            print(row)

        cursor.close()
        conn.close()

    except mysql.connector.Error as err:
        print("Report Error:", err)

# store data to csv and txt
def export_report():
    try:
        conn = mysql.connector.connect(
            host="localhost",
            user="root",
            password=os.getenv("Database_Password"),
            database="dog_db"
        )
        # Query for export
        query = """
        SELECT name, life_span, temperament, origin, breed_group, weight, height
        FROM dogs
        WHERE origin IS NOT NULL
        """

        df = pd.read_sql(query, conn)

        # Export to CSV
        df.to_csv("dog_report.csv", index=False)

        print(f"CSV exported successfully to dog_report.csv")

        # Export to TXT
        txt_file = "dog_report.txt"

        with open("dog_report.txt", "w", encoding="utf-8") as file:
            file.write("DOG BREED REPORT\n")
            file.write(df.to_string(index=False))

        print(f"TXT exported successfully to dog_report.txt")

        conn.close()

    except Exception as e:
        print("Export Error:", e)

if __name__ == "__main__":
    create_database()
    create_table()

    data = fetch_data()

    if data:
        store_data(data)
        run_report()
        export_report()
    else:
        print("No data fetched. Program stopped.")