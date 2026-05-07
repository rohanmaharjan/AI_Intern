'''
COMPREHENSIVE MULTI-TABLE RELATIONAL DATABASE SYSTEM
This script creates a MySQL database (store_db) with three interconnected tables:
- customers: stores customer information and city
- products: stores product details and prices
- orders: links customers to products with order quantities

The script demonstrates:
1. Database and table creation with proper relationships
2. Parameterized queries to prevent SQL injection
3. Complex SQL queries with JOINs, GROUP BY, and HAVING clauses
4. CSV export of results
'''

import mysql.connector
from dotenv import load_dotenv
import os
from datetime import datetime, timedelta
import random
import csv

load_dotenv()

# DATABASE CONNECTION
def create_connection():
    try:
        conn = mysql.connector.connect(
            host='localhost',
            user='root',
            password=os.getenv("Database_Password")
        )

        print("MySQL server connected!")
        cursor = conn.cursor()

        return conn, cursor

    except mysql.connector.Error as e:
        print(f"Error connecting to MySQL: {e}")
        return None, None


# CREATE DATABASE
def create_database(conn, cursor):
    try:
        cursor.execute("DROP DATABASE IF EXISTS store_db")
        print("\nDropped existing store_db database")

        cursor.execute("CREATE DATABASE IF NOT EXISTS store_db")
        print("\nNew database created")

    except mysql.connector.Error as e:
        print(f"Error creating database: {e}")

    finally:
        cursor.close()


# CREATE TABLES
def create_table(conn, cursor):
    try:
        cursor.execute("USE store_db")

        # CUSTOMERS TABLE
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

        # PRODUCTS TABLE
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

        # ORDERS TABLE
        create_orders_table = """
        CREATE TABLE IF NOT EXISTS orders (
            order_id INT AUTO_INCREMENT PRIMARY KEY,
            customer_id INT NOT NULL,
            product_id INT NOT NULL,
            quantity INT NOT NULL DEFAULT 1,
            order_date DATE NOT NULL,

            FOREIGN KEY (customer_id)
            REFERENCES customers(customer_id)
            ON DELETE CASCADE,

            FOREIGN KEY (product_id)
            REFERENCES products(product_id)
            ON DELETE CASCADE
        )
        """

        cursor.execute(create_orders_table)
        print("\nCreated orders table with foreign keys")

        conn.commit()

    except mysql.connector.Error as e:
        print(f"Error creating tables: {e}")

    finally:
        cursor.close()


# INSERT DATA
def insert_data(conn, cursor):
    try:
        cursor.execute("USE store_db")

        # INSERT CUSTOMERS
        customers_data = [
            ("Rajesh Kumar", "Kathmandu", "rajesh@email.com"),
            ("Priya Singh", "Lalitpur", "priya@email.com"),
            ("Amit Patel", "Kathmandu", "amit@email.com"),
            ("Deepika Sharma", "Bhaktapur", "deepika@email.com"),
            ("Vikram Joshi", "Kathmandu", "vikram@email.com"),
            ("Neha Gupta", "Lalitpur", "neha@email.com"),
            ("Arjun Verma", "Kathmandu", "arjun@email.com"),
            ("Sakshi Desai", "Bhaktapur", "sakshi@email.com"),
            ("Rohan Kapoor", "Kathmandu", "rohan@email.com"),
            ("Ananya Mishra", "Lalitpur", "ananya@email.com"),
        ]

        insert_customers = """
        INSERT INTO customers (name, city, email)
        VALUES (%s, %s, %s)
        """

        cursor.executemany(insert_customers, customers_data)

        conn.commit()
        print(f"\nInserted {len(customers_data)} customers")

        # INSERT PRODUCTS
        products_data = [
            ("Laptop", "Electronics", 1200.00),
            ("Mouse", "Electronics", 25.00),
            ("Keyboard", "Electronics", 75.00),
            ("Monitor", "Electronics", 300.00),
            ("Headphones", "Electronics", 150.00),
            ("USB Cable", "Electronics", 10.00),
            ("Phone Stand", "Accessories", 20.00),
            ("Laptop Bag", "Accessories", 50.00),
        ]

        insert_products = """
        INSERT INTO products (name, category, price)
        VALUES (%s, %s, %s)
        """

        cursor.executemany(insert_products, products_data)

        conn.commit()
        print(f"Inserted {len(products_data)} products")

        # INSERT ORDERS
        orders_data = []

        base_date = datetime(2026, 1, 1)

        for _ in range(20):
            customer_id = random.randint(1, 10)
            product_id = random.randint(1, 8)
            quantity = random.randint(1, 5)

            order_date = base_date + timedelta(
                days=random.randint(0, 180)
            )

            orders_data.append((
                customer_id,
                product_id,
                quantity,
                order_date.strftime('%Y-%m-%d')
            ))

        insert_orders = """
        INSERT INTO orders
        (customer_id, product_id, quantity, order_date)
        VALUES (%s, %s, %s, %s)
        """

        cursor.executemany(insert_orders, orders_data)

        conn.commit()
        print(f"Inserted {len(orders_data)} orders")

    except mysql.connector.Error as e:
        print(f"Error inserting data: {e}")
        conn.rollback()

    finally:
        cursor.close()


# SOLVE QUERIES
def solve_queries(conn, cursor):

    revenue_results = []

    try:
        cursor.execute("USE store_db")

        # QUERY 1
        query_one = """
        SELECT
            c.customer_id,
            c.name,
            c.city,
            SUM(p.price * o.quantity) AS total_spent
        FROM customers c
        INNER JOIN orders o ON c.customer_id = o.customer_id
        INNER JOIN products p ON o.product_id = p.product_id
        GROUP BY c.customer_id, c.name, c.city
        ORDER BY total_spent DESC
        """

        cursor.execute(query_one)

        revenue_results = cursor.fetchall()

        print("\nRevenue per customer:\n")

        for row in revenue_results:
            print(row)

        # QUERY 2
        query_two = """
        SELECT
            p.product_id,
            p.name,
            p.category,
            SUM(o.quantity) AS total_quantity
        FROM products p
        INNER JOIN orders o ON p.product_id = o.product_id
        GROUP BY p.product_id, p.name, p.category
        ORDER BY total_quantity DESC
        LIMIT 1
        """

        cursor.execute(query_two)

        result = cursor.fetchone()

        print("\nMost ordered product by quantity:\n")
        print(result)

        # QUERY 3
        query_three = """
        SELECT
            c.customer_id,
            c.name,
            c.city,
            COUNT(o.order_id) AS order_count
        FROM customers c
        LEFT JOIN orders o ON c.customer_id = o.customer_id
        GROUP BY c.customer_id, c.name, c.city
        HAVING COUNT(o.order_id) > 2
        ORDER BY order_count DESC
        """

        cursor.execute(query_three)

        print("\nCustomers with more than 2 orders:\n")

        for row in cursor.fetchall():
            print(row)

        # QUERY 4
        query_four = """
        SELECT
            c.city,
            COUNT(o.order_id) AS total_orders,
            AVG(p.price * o.quantity) AS avg_order_value
        FROM customers c
        INNER JOIN orders o
        ON c.customer_id = o.customer_id
        INNER JOIN products p
        ON o.product_id = p.product_id
        GROUP BY c.city
        ORDER BY avg_order_value DESC
        """

        cursor.execute(query_four)

        print("\nAverage order value per city:\n")

        for row in cursor.fetchall():
            print(row)

    except mysql.connector.Error as e:
        print(f"Database Error: {e}")

    finally:
        cursor.close()

    return revenue_results


# EXPORT CSV
def export_to_csv(filename, headers, data):

    try:
        with open(filename, "w", newline="", encoding="utf-8") as file:

            writer = csv.DictWriter(file, fieldnames=headers)

            writer.writeheader()

            writer.writerows(data)

        print(f"\nSuccessfully exported data to {filename}")

    except IOError as e:
        print(f"CSV Export Error: {e}")


# MAIN FUNCTION
def main():

    conn, cursor = create_connection()

    if conn is None:
        return

    create_database(conn, cursor)

    cursor = conn.cursor()
    create_table(conn, cursor)

    cursor = conn.cursor()
    insert_data(conn, cursor)

    cursor = conn.cursor()
    revenue_data = solve_queries(conn, cursor)

    export_data = []

    for row in revenue_data:

        export_data.append({
            "Customer ID": row[0],
            "Name": row[1],
            "City": row[2],
            "Total Spent": f"${row[3]:.2f}"
        })

    export_to_csv(
        "revenue_data.csv",
        ["Customer ID", "Name", "City", "Total Spent"],
        export_data
    )

    conn.close()
    print("\nDatabase connection closed")


if __name__ == "__main__":
    main()