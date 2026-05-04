'''COMPREHENSIVE MULTI-TABLE RELATIONAL DATABASE SYSTEM
This script creates a MySQL database (store_db) with three interconnected tables:
- customers: stores customer information and city
- products: stores product details and prices
- orders: links customers to products with order quantities
 
The script demonstrates:
1. Database and table creation with proper relationships
2. Parameterized queries to prevent SQL injection
3. Complex SQL queries with JOINs, GROUP BY, and HAVING clauses
4. CSV export of results'''

import mysql.connector
from dotenv import load_dotenv
import os

load_dotenv()

# database connection

def create_connection():
    try:
        cnn = mysql.connector.connect(
            host='localhost',
            user='root',
            password=os.getenv("Database_Password")
        )
        print("MySQL server connected!")
        cursor = cnn.cursor()
        return cnn,cursor
    except mysql.connector.Error as e:
        print(f"Error connecting to MySQL: {e}")
        return None
    
def create_database(cnn,cursor):
    try:
        cursor.execute("DROP DATABASE IF EXISTS store_db")
        print("\nDropped existing store_db database")
        cursor.execute("CREATE DATABASE IF NOT EXISTS store_db")
        print("\nNEw database created")
    except mysql.connector.Error as e:
        print(f"Error creating database: {e}")
    finally:
        cursor.close()

def create_table(conn,cursor):
    try:
        # Switch to our database
        cursor.execute("USE store_db")
        
        # TABLE 1: CUSTOMERS
        create_customers_table = """
        CREATE TABLE IF NOT EXISTS customers (
            customer_id INT AUTO_INCREMENT PRIMARY KEY,
            name VARCHAR(100) NOT NULL,
            city VARCHAR(50) NOT NULL,
            email VARCHAR(100) NOT NULL UNIQUE
        )
        """
        cursor.execute(create_customers_table)
        print("\nCreated customers table")
        
        # TABLE 2: PRODUCTS
        create_products_table = """
        CREATE TABLE IF NOT EXISTS products (
            product_id INT AUTO_INCREMENT PRIMARY KEY,
            name VARCHAR(100) NOT NULL,
            category VARCHAR(50) NOT NULL,
            price DECIMAL(10, 2) NOT NULL
        )
        """
        cursor.execute(create_products_table)
        print("\nCreated products table")
        
        # TABLE 3: ORDERS (JUNCTION TABLE WITH FOREIGN KEYS)
        create_orders_table = """
        CREATE TABLE IF NOT EXISTS orders (
            order_id INT AUTO_INCREMENT PRIMARY KEY,
            customer_id INT NOT NULL,
            product_id INT NOT NULL,
            quantity INT NOT NULL DEFAULT 1,
            order_date DATE NOT NULL,
            FOREIGN KEY (customer_id) REFERENCES customers(customer_id) ON DELETE CASCADE,
            FOREIGN KEY (product_id) REFERENCES products(product_id) ON DELETE CASCADE
        )
        """
        cursor.execute(create_orders_table)
        print("\nCreated 'orders' table with foreign key relationships")
        
        conn.commit()
    except mysql.connector.Error as e:
        print(f"Error creating tables: {e}")
    finally:
        cursor.close()
    

def main():
    conn, cursor = create_connection()
    if conn is None:
        return
    
    create_database(conn, cursor)

    # Need new cursor because previous one was closed
    cursor = conn.cursor()
    create_table(conn, cursor)

    conn.close()

if __name__ == "__main__":
    main()