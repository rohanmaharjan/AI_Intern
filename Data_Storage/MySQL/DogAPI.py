import requests
import mysql.connector
from dotenv import load_dotenv
import os

load_dotenv()

#create database
def create_database():
    try:
        conn = mysql.connector.conect(
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
        conn = mysql.connector.connect(
            host="localhost",
            user="root",
            password=os.getenv("Database_Password"),
            database="dog_db"
        )

        cursor = conn.cursor() 

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


create_table()

# fetch data from API
def fetch_data():
    url = "https://api.thedogapi.com/v1/breeds"

    params = {
        "API_KEY": os.getenv("API_KEY")
    }

    try:
        response = requests.get(url, params=params, timeout=10)

        response.raise_for_stauts()

        dog_data = response.json()

        print(f'fetched {len(dog_data)} dog breeds successfully')
        return dog_data
    
    except requests.exceptions.timeout:
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
    

    


