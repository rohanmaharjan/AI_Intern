import requests, csv
import mysql.connector
from dotenv import load_dotenv
import os

load_dotenv()

url = "https://jsonplaceholder.typicode.com/users"

response = requests.get(url)


users = response.json() # Parse JSON

# Connect to MySQL server
conn = mysql.connector.connect(
    host= "localhost",
    user= "root",
    password= os.getenv("Database_Password"),
    database= "app"
)

cursor = conn.cursor()

# Create app.db with a users table: id, name, email, phone, city, company_name

cursor.execute("""
CREATE TABLE IF NOT EXISTS users(
    id INT PRIMARY KEY,
    name varchar(50) NOT NULL,
    email VARCHAR(50) UNIQUE,
    phone VARCHAR(50) UNIQUE,
    city VARCHAR(100),
    company_name VARCHAR(100)
)
""")

# 2. Collect ALL users into one list FIRST
users_data = []
for user in users:
    users_data.append((
        user["id"], 
        user["name"], 
        user["email"], 
        user["phone"], 
        user["address"]["city"], 
        user["company"]["name"]
    ))

insert_users = """
INSERT INTO users (id, name, email, phone, city, company_name)
VALUES (%s, %s, %s, %s, %s, %s)
ON DUPLICATE KEY UPDATE
name = VALUES(name),
email = VALUES(email),
phone = VALUES(phone),
city = VALUES(city),
company_name = VALUES(company_name)
"""

# pass complete list ot executemany
cursor.executemany(insert_users, users_data )

conn.commit()

print("Data successfully synced!")
cursor.close()
conn.close()