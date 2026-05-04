# Week 3 – Data Storage & MySQL (Data Engineering Foundations)
## 📌 Overview

This project focuses on storing, managing, and querying data using MySQL.  
It builds on previous work with APIs and data fetching by introducing structured storage and database operations.

Across 5 tasks, I implemented:
- Database creation and querying
- API to MySQL pipelines
- Data analysis using SQL
- Data updates and integrity handling
- A complete end-to-end data system

The goal was to understand how real-world data systems move from raw data → structured storage → insights.
## 🧠 Key Concepts Learned

### 1. Data Types
- Structured (SQL tables, CSV)
- Unstructured (images, text)
- Semi-structured (JSON, APIs)

### 2. Why Databases Matter
- Efficient querying vs CSV loops
- Data integrity (types, constraints)
- Scalability for large datasets
- Concurrent access support

### 3. SQL Fundamentals
- CREATE, INSERT, SELECT, UPDATE, DELETE
- Filtering using WHERE
- Aggregations using GROUP BY
- Sorting using ORDER BY

### 4. Python + MySQL Integration
- Connecting using `mysql.connector`
- Executing queries via cursor
- Fetching results (`fetchall`, `fetchone`)
- Preventing SQL injection using placeholders

### 5. Data Pipelines
- API → JSON → Database → Query → Output
## 🛠️ Tech Stack

- Python
- MySQL
- mysql-connector-python
- Requests (API handling)
- CSV / File handling
## ✅ Task 1: Library Database

- Created `library.db` with books table
- Inserted 8+ records with diverse data
- Performed queries:
  - Books after 2000 (sorted by rating)
  - Fiction books with rating > 4
  - Average rating calculation
  - Count of books per genre (GROUP BY)

🔍 Key Learning:
- Writing structured SQL queries
- Using aggregation functions
## ✅ Task 2: API to MySQL Pipeline

- Fetched user data from JSONPlaceholder API
- Stored in `app.db`
- Extracted nested JSON fields (city, company)
- Created second table `posts`
- Filtered posts by specific users

🔍 Key Learning:
- Handling API data (JSON → structured format)
- Working with relational tables
- Using GROUP BY and JOIN
## ✅ Task 3: Weather Data + Analysis

- Collected 7-day weather data for 3 cities
- Stored in `weather.db`
- Inserted 21 records
- Performed analysis:
  - Highest average temperature
  - Hottest day overall
  - Large temperature differences

- Exported summary to `summary.txt`

🔍 Key Learning:
- Real-world data analysis using SQL
- Combining Python + SQL for reporting
## ✅ Task 4: Grades Management System

- Created `grades.db`
- Inserted 15 student records
- Assigned grades using Python logic
- Updated database dynamically
- Deleted failing students (<50)
- Added new column using ALTER TABLE

🔍 Key Learning:
- Data integrity handling
- UPDATE, DELETE operations
- Schema modification
## ✅ Task 5: Full Data System

- Built complete pipeline:
  API → Fetch → Store → Query → Export

Features:
- Error handling using try/except
- Reusable functions:
  - fetch_data()
  - store_data()
  - run_report()
- Exported results to CSV and TXT

🔍 Key Learning:
- End-to-end system design
- Writing production-style code
## 💡 Key Takeaways

- Databases are essential for scalable data systems
- SQL is powerful for querying and analysis
- APIs provide semi-structured data that must be cleaned before storage
- Python acts as the glue between systems
- Writing clean, modular code improves maintainability
## ⚠️ Challenges Faced

- Handling nested JSON data from APIs
- Designing proper database schema
- Avoiding SQL injection
- Managing database connections efficiently
- Debugging SQL queries
## ▶️ How to Run

1. Install dependencies:
   pip install mysql-connector-python requests

2. Start MySQL server

3. Run scripts:
   python task1_library.py
   python task2_api_pipeline.py
   ...

4. Check databases and outputs