'''
Task 01 · Create, Insert & Query [Medium]
Independent task — build your first MySQL database from scratch
Goal:
Create a MySQL database, populate it with data, and run queries to answer questions about it.
1. Create a database called library.db with a table books
   (id, title, author, year, genre, rating REAL)
2. Insert at least 8 books — use a mix of genres, years, and ratings
3. Query 1:
   SELECT all books published after 2000, ordered by rating (highest first)
4. Query 2:
   SELECT all books in the 'Fiction' genre with rating above 4.0
5. Query 3:
   Find the average rating across all books
6. Query 4:
   Count how many books exist per genre — use GROUP BY genre
7. Print all query results neatly with labels — not just raw tuples
'''

import mysql.connector
from dotenv import load_dotenv
import os

load_dotenv()

# Connect to MySQL server
conn = mysql.connector.connect(
    host="localhost",
    user="root",
    password = os.getenv("Database_Password"),
    database="library"
)

cursor = conn.cursor()

# CREATE TABLE: books
cursor.execute("""
CREATE TABLE IF NOT EXISTS books (
    id INT PRIMARY KEY,
    title VARCHAR(255) NOT NULL,
    author VARCHAR(255) NOT NULL,
    year INT,
    genre VARCHAR(100),
    rating FLOAT
)
""")

# INSERT DATA INTO books
books_data = [
    (1, "Atomic Habits", "James Clear", 2018, "Self Help", 4.8),
    (2, "Harry Potter", "J.K. Rowling", 1997, "Fiction", 4.7),
    (3, "The Alchemist", "Paulo Coelho", 1988, "Fiction", 4.3),
    (4, "Rich Dad Poor Dad", "Robert Kiyosaki", 1997, "Finance", 4.5),
    (5, "The Psychology of Money", "Morgan Housel", 2020, "Finance", 4.6),
    (6, "Ikigai", "Hector Garcia", 2016, "Self Help", 4.4),
    (7, "Deep Work", "Cal Newport", 2016, "Productivity", 4.2),
    (8, "The Silent Patient", "Alex Michaelides", 2019, "Fiction", 4.1)
]

insert_books = """
INSERT INTO books (id, title, author, year, genre, rating)
VALUES (%s, %s, %s, %s, %s, %s)
ON DUPLICATE KEY UPDATE
title = VALUES(title),
author = VALUES(author),
year = VALUES(year),
genre = VALUES(genre),
rating = VALUES(rating)
"""

cursor.executemany(insert_books, books_data)

# BONUS: CREATE TABLE reviews
# Linked with books using book_id
cursor.execute("""
CREATE TABLE IF NOT EXISTS reviews (
    review_id INT PRIMARY KEY,
    book_id INT,
    review TEXT,
    FOREIGN KEY (book_id) REFERENCES books(id)
)
""")

# INSERT DATA INTO reviews
reviews_data = [
    (1, 1, "Excellent book for building good habits"),
    (2, 2, "Magical and exciting story"),
    (3, 5, "Very practical financial advice"),
    (4, 8, "Thrilling psychological mystery")
]

insert_reviews = """
INSERT INTO reviews (review_id, book_id, review)
VALUES (%s, %s, %s)
ON DUPLICATE KEY UPDATE
review = VALUES(review)
"""

cursor.executemany(insert_reviews, reviews_data)

# Save all changes
conn.commit()

# QUERY 1
# Books published after 2000, ordered by rating (highest first)
print("\n--- Query 1: Books published after 2000 ordered by rating ---")

cursor.execute("""
SELECT * FROM books
WHERE year > 2000
ORDER BY rating DESC
""")

for row in cursor.fetchall():
    print(f"ID: {row[0]}, Title: {row[1]}, Author: {row[2]}, Year: {row[3]}, Genre: {row[4]}, Rating: {row[5]}")

# QUERY 2
# Fiction books with rating > 4.0
print("\n--- Query 2: Fiction books with rating above 4.0 ---")

cursor.execute("""
SELECT * FROM books
WHERE genre = 'Fiction'
AND rating > 4.0
""")

for row in cursor.fetchall():
    print(f"ID: {row[0]}, Title: {row[1]}, Author: {row[2]}, Rating: {row[5]}")

# QUERY 3
# Average rating of all books
print("\n--- Query 3: Average rating of all books ---")

cursor.execute("""
SELECT AVG(rating) FROM books
""")

avg_rating = cursor.fetchone()[0]
print(f"Average Rating: {avg_rating:.2f}")

# -----------------------------------
# QUERY 4
# Count books per genre
# -----------------------------------
print("\n--- Query 4: Number of books per genre ---")

cursor.execute("""
SELECT genre, COUNT(*)
FROM books
GROUP BY genre
""")

for row in cursor.fetchall():
    print(f"Genre: {row[0]}, Total Books: {row[1]}")

# BONUS QUERY
# Show books with their reviews
print("\n--- Bonus Query: Books with Reviews ---")

cursor.execute("""
SELECT books.title, reviews.review
FROM books
JOIN reviews
ON books.id = reviews.book_id
""")

for row in cursor.fetchall():
    print(f"Book: {row[0]} -> Review: {row[1]}")

# Close connection
cursor.close()
conn.close()

print("\nMySQL Library Database Task Completed Successfully.")