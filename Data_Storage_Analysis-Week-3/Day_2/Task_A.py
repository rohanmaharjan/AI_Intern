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
from datetime import datetime,timedelta
import random
import csv

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

def insert_data(conn, cursor):
    try:
        cursor.execute("USE store_db")     
        print("\nStarting customer insertion...")
        
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
        
        # Parameterized query - %s placeholders are safe
        insert_customers = "INSERT INTO customers (name, city, email) VALUES (%s, %s, %s)"
        
        for customer in customers_data:
            # Pass the tuple as second parameter - database driver handles escaping
            cursor.execute(insert_customers, customer)
        
        conn.commit()
        print(f"Inserted {len(customers_data)} customers")
        
        # Insert products
        print("Starting product insertion...")
        
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
        
        insert_products = "INSERT INTO products (name, category, price) VALUES (%s, %s, %s)"
        
        for product in products_data:
            cursor.execute(insert_products, product)
        
        conn.commit()
        print(f"Inserted {len(products_data)} products")
        
        # insert orders
        print("Starting order insertion...")
        
        # Generate 20 orders with random combinations
        orders_data = []
        base_date = datetime(2026, 1, 1)
        
        # We create 20 orders spread across our 10 customers
        for i in range(20):
            customer_id = (i % 10) + 1  # Cycle through customers 1-10
            product_id = random.randint(1, 8)  # Random product 1-8
            quantity = random.randint(1, 5)  # Random quantity 1-5
            # Spread orders across 6 months
            order_date = base_date + timedelta(days=random.randint(0, 180))
            
            orders_data.append((customer_id, product_id, quantity, order_date.strftime('%Y-%m-%d')))
        
        insert_orders = "INSERT INTO orders (customer_id, product_id, quantity, order_date) VALUES (%s, %s, %s, %s)"
        
        for order in orders_data:
            cursor.execute(insert_orders, order)
        
        conn.commit()
        print(f"Inserted {len(orders_data)} orders")
        
    except mysql.connector.Error as e:
        print(f"Error inserting data: {e}")
        conn.rollback()  # Undo any partial insertions
    finally:
        cursor.close()

def solve_queries(conn, cursor):
    # Query 1:Total Money Spent Per Customer
    try:
        cursor.execute("USE store_db")
        
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
        results = cursor.fetchall()
        print("\nRevenue per Customers: \n")
        for row in results:
            print(row)
        
        
    except mysql.connector.Error as e:
        print(f"Error in Query 1: {e}")
        return []
    
    # Query 2:Most Ordered Product By Total Quantity
    try:
        cursor.execute("USE store_db")
        
        query_two = """
        SELECT 
            p.product_id,
            p.name,
            p.category,
            SUM(o.quantity) AS total_quantity
        FROM products p
        LEFT JOIN orders o ON p.product_id = o.product_id
        GROUP BY p.product_id, p.name, p.category
        ORDER BY total_quantity DESC
        LIMIT 1
        """
        
        cursor.execute(query_two)
        # result = cursor.fetchone()  # Get only the first (top) result
        # return result
        print("\nMost ordered product by total quantity")
        for row in cursor.fetchone():
            print(row)
        
    except mysql.connector.Error as e:
        print(f"Error in Query 1: {e}")
        return []
    
    # QUERY 3: Customers Who Placed More Than 2 Orders

    try:
        cursor.execute("USE store_db")
        
        query_three = """
        SELECT 
            c.customer_id,
            c.name,
            c.city,
            COUNT(o.order_id) AS order_count
        FROM customers c
        INNER JOIN orders o ON c.customer_id = o.customer_id
        GROUP BY c.customer_id, c.name, c.city
        HAVING COUNT(o.order_id) > 2
        ORDER BY order_count DESC
        """
        
        cursor.execute(query_three)
        # results = cursor.fetchall()
        # return results
        print("\nCustomers who placed more than 2 orders: \n")
        for row in cursor.fetchall():
            print(row)
        
    except mysql.connector.Error as e:
        print(f"✗ Error in Query 3: {e}")
        return []
    
    # QUERY 4: Average Order Value Per City (GROUP BY + AVG + Multiple Joins)
    try:
        cursor.execute("USE store_db")
        
        query_four = """
        SELECT 
            c.city,
            COUNT(o.order_id) AS total_orders,
            AVG(p.price * o.quantity) AS avg_order_value
        FROM customers c
        INNER JOIN orders o ON c.customer_id = o.customer_id
        INNER JOIN products p ON o.product_id = p.product_id
        GROUP BY c.city
        ORDER BY avg_order_value DESC
        """
        
        cursor.execute(query_four)
        # results = cursor.fetchall()
        # return results
        print("\nAverage order value per city:\n")
        for row in cursor.fetchall():
            print(row)
        
    except mysql.connector.Error as e:
        print(f"✗ Error in Query 4: {e}")
        return []
    finally:    
        cursor.close()
        return results

def export_to_csv(filename,headers,data):
    try:
        with open(filename, 'w', newline='', encoding='utf-8') as csvfile:
            # DictWriter allows us to write dictionaries as rows
            writer = csv.DictWriter(csvfile, fieldnames=headers)
            
            # Write header row
            writer.writeheader()
            
            # Write all data rows
            writer.writerows(data)
        
        print(f"✓ Successfully exported results to {filename}")
        
    except IOError as e:
        print(f"✗ Error writing CSV file: {e}")


def main():
    conn, cursor = create_connection()
    if conn is None:
        return
    
    create_database(conn, cursor)

    # Need new cursor because previous one was closed
    cursor = conn.cursor()
    create_table(conn, cursor)

    cursor = conn.cursor()
    insert_data(conn, cursor)

    cursor = conn.cursor()
    

    revenue_data = solve_queries(conn, cursor)
    if revenue_data:
        # Prepare data for CSV export
        export_data = []
        for row in revenue_data:
            export_data.append({
                'Customer ID': row[0],
                'Name': row[1],
                'City': row[2],
                'Total Spent': f"${row[3]:.2f}"
            })

    export_to_csv('revenue_data.csv',['Customer ID', 'Name', 'City', 'Total Spent'],export_data)

    conn.close()

if __name__ == "__main__":
    main()