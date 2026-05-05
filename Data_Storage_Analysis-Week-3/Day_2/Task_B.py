import requests
import mysql.connector
from datetime import datetime
from dotenv import load_dotenv
import os

load_dotenv()

# DATABASE CONFIG
DB_CONFIG = {
    "host": "localhost",
    "user": "root",
    "password": os.getenv("Database_Password")
}

DB_NAME = "monitor_db"
API_URL = "https://jsonplaceholder.typicode.com/posts"


# CONNECT TO MYSQL SERVER
def connect_mysql():
    try:
        conn = mysql.connector.connect(**DB_CONFIG)
        return conn
    except Exception as e:
        print("Error connecting to MySQL:", e)
        return None


# CREATE DATABASE & TABLES
def setup_database():
    conn = connect_mysql()
    if not conn:
        return

    cursor = conn.cursor()

    try:
        cursor.execute(f"CREATE DATABASE IF NOT EXISTS {DB_NAME}")
        conn.database = DB_NAME

        # POSTS TABLE
        cursor.execute("""
        CREATE TABLE IF NOT EXISTS posts (
            id INT PRIMARY KEY,
            user_id INT,
            title TEXT,
            body TEXT,
            last_updated TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP
        )
        """)

        # CHANGE LOG TABLE
        cursor.execute("""
        CREATE TABLE IF NOT EXISTS change_log (
            log_id INT AUTO_INCREMENT PRIMARY KEY,
            post_id INT,
            user_id INT,
            change_type VARCHAR(20),
            old_title TEXT,
            new_title TEXT,
            changed_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
        """)

        conn.commit()
        print("Database and tables ready.")

    except Exception as e:
        print("Error creating database/tables:", e)

    finally:
        cursor.close()
        conn.close()


# FETCH API DATA
def fetch_posts():
    try:
        response = requests.get(API_URL)
        response.raise_for_status()
        return response.json()
    except Exception as e:
        print("Error fetching API:", e)
        return []


# PROCESS DATA (CHANGE DETECTION)
def process_posts(posts_data):
    try:
        conn = mysql.connector.connect(**DB_CONFIG, database=DB_NAME)
        cursor = conn.cursor(dictionary=True)

        run_timestamp = datetime.now()

        for post in posts_data:
            try:
                # Check if exists
                cursor.execute("SELECT * FROM posts WHERE id = %s", (post['id'],))
                existing = cursor.fetchone()

                if not existing:
                    # NEW POST
                    cursor.execute("""
                        INSERT INTO posts (id, user_id, title, body)
                        VALUES (%s, %s, %s, %s)
                    """, (post['id'], post['userId'], post['title'], post['body']))

                    cursor.execute("""
                        INSERT INTO change_log (post_id, user_id, change_type, old_title, new_title, changed_at)
                        VALUES (%s, %s, 'NEW', NULL, %s, %s)
                    """, (post['id'], post['userId'], post['title'], run_timestamp))

                else:
                    # CHECK MODIFICATION
                    if existing['title'] != post['title'] or existing['body'] != post['body']:
                        cursor.execute("""
                            UPDATE posts
                            SET title=%s, body=%s
                            WHERE id=%s
                        """, (post['title'], post['body'], post['id']))

                        cursor.execute("""
                            INSERT INTO change_log (post_id, user_id, change_type, old_title, new_title, changed_at)
                            VALUES (%s, %s, 'MODIFIED', %s, %s, %s)
                        """, (
                            post['id'],
                            post['userId'],
                            existing['title'],
                            post['title'],
                            run_timestamp
                        ))

            except Exception as inner_e:
                print(f"Error processing post {post['id']}:", inner_e)

        conn.commit()
        print("Processing complete.")

    except Exception as e:
        print("Error in processing:", e)

    finally:
        cursor.close()
        conn.close()


# ANALYTICS OUTPUT
def print_reports():
    try:
        conn = mysql.connector.connect(**DB_CONFIG, database=DB_NAME)
        cursor = conn.cursor()

        print("\n--- Post Count Per User ---")
        cursor.execute("""
            SELECT user_id, COUNT(*) 
            FROM posts 
            GROUP BY user_id
        """)
        for row in cursor.fetchall():
            print(f"User {row[0]} : {row[1]} posts")

        print("\n--- Latest Run Change Logs ---")
        cursor.execute("""
            SELECT * FROM change_log
            WHERE changed_at >= (SELECT MAX(changed_at) FROM change_log)
        """)
        for row in cursor.fetchall():
            print(row)

        print("\n--- User With Most Changes ---")
        cursor.execute("""
            SELECT user_id, COUNT(*) AS changes_count
            FROM change_log
            GROUP BY user_id
            ORDER BY changes_count DESC
            LIMIT 1
        """)
        result = cursor.fetchone()
        if result:
            print(f"User {result[0]} : {result[1]} changes")

    except Exception as e:
        print("Error generating reports:", e)

    finally:
        cursor.close()
        conn.close()


# MAIN EXECUTION
if __name__ == "__main__":
    print("Starting API Monitor...")

    setup_database()

    posts = fetch_posts()
    if posts:
        process_posts(posts)

    print_reports()

    print("\nDone.")