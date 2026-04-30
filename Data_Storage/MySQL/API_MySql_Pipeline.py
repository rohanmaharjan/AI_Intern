import requests
import mysql.connector
from dotenv import load_dotenv
import os

load_dotenv()

url_users = "https://jsonplaceholder.typicode.com/users"
url_posts = "https://jsonplaceholder.typicode.com/posts"

# fetch for users
try:
    response = requests.get(url_users)
    response.raise_for_status()
    users = response.json()
    print("Users API fetched successfully!")
except requests.exceptions.RequestException as e:
    print("Error fetching users API:", e)
    exit()

users = response.json() # Parse JSON

# Connect to MySQL server
try:
    conn = mysql.connector.connect(
    host= "localhost",
    user= "root",
    password= os.getenv("Database_Password"),
    database= "app"
    )
    cursor = conn.cursor()
    print("Connected to MySQL successfully!")

except mysql.connector.Error as err:
    print("Database Connection Error:", err)
    exit()

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

# Query 1
# print all users sorted alphabetically by Ascending order
print("\n--- Lists of All Users in Ascending Order ---")

cursor.execute("""
SELECT * FROM users
ORDER BY name ASC
""")

for row in cursor.fetchall():
    print(f"ID: { row[0]}, Nanme: {row[1]}, Email: {row[2]}, Phone: {row[3]} , City: {row[4]},Company Name: {row[5]}")

# Query 2
# Find users from the same city (GROUP BY city, HAVING COUNT > 1)

print("\n--- Lists of users form same city ---")

cursor.execute("""
SELECT city, COUNT(*) AS total_users
FROM users
GROUP BY city
HAVING COUNT(*) > 1
""")

results = cursor.fetchall()

for row in results:
    print(f"City: {row[0]}, Total Users: {row[1]}")

# creating table posts
cursor.execute(
"""
CREATE TABLE IF NOT EXISTS posts(
    id INT PRIMARY KEY,
    user_id INT,
    title TEXT,
    body TEXT,
    FOREIGN KEY (user_id) REFERENCES users(id)
)
"""
)

# fetch for posts
try:
    response = requests.get(url_posts)
    response.raise_for_status()
    posts = response.json()
    print("Posts API fetched successfully!")
except requests.exceptions.RequestException as e:
    print("Error fetching posts API:", e)
    exit()

posts = response.json()

# filter posts only by user_id 1, 2, 3
posts_data = []
for post in posts:
    if post["userId"] in [1, 2, 3]:
        posts_data.append((
            post["id"],
            post["userId"],
            post["title"],
            post["body"]
        ))

insert_posts = """
INSERT INTO posts (id, user_id, title, body)
VALUES (%s, %s, %s, %s)
ON DUPLICATE KEY UPDATE
title = VALUES(title),
body = VALUES(body)
"""

cursor.executemany( insert_posts, posts_data)
conn.commit()
print("Posts data inserted successfully")

# BONUS CHECK
# Show inserted posts
print("\n--- Posts inserted for user_id 1, 2, 3 ---")

cursor.execute("""
SELECT id, user_id, title
FROM posts
ORDER BY user_id
""")

results = cursor.fetchall()

for row in results:
    print(
        f"Post ID: {row[0]}, "
        f"User ID: {row[1]}, "
        f"Title: {row[2]}"
    )

# close connections
cursor.close()
conn.close()