# Fault-Tolerant ETL Pipelines and Data Engineering Capstone

## Project Overview

This project contains three advanced ETL (Extract, Transform, Load) tasks focused on building production-style data pipelines using Python, Pandas, SQLAlchemy, and MySQL.

The project demonstrates:

- Multi-source data extraction
- Fault-tolerant API handling
- Data cleaning and transformation
- Conflict resolution strategies
- Data quality auditing
- Logging and modular pipeline design
- Idempotent database loading
- Feature engineering and enrichment
- MySQL integration using SQLAlchemy

The datasets were extracted from the public API:

- [JSONPlaceholder API](https://jsonplaceholder.typicode.com?utm_source=chatgpt.com)

---

# Technologies Used

- Python
- Pandas
- SQLAlchemy
- MySQL
- Requests / urllib
- dotenv
- Logging module
- CSV handling

---

# Task 1 — Fault-Tolerant Multi-Source ETL Pipeline

## Objective

Build an ETL pipeline that extracts data from multiple sources and resolves conflicting records before loading into MySQL and CSV.

## Features Implemented

### Multi-Source Extraction

Data was extracted from:

- `/users` API endpoint
- `/posts` API endpoint
- Local messy CSV file

### Fault Tolerance

Implemented:

- `try-except` blocks
- Timeout handling
- HTTP status code checks
- Retry logic for failed API calls

### JSON Normalization

Nested JSON fields were flattened using:

```python
pd.json_normalize()
```

Example:

```python
address.city
company.name
```

### Conflict Resolution Strategy

When the same email existed in both datasets with different names:

- API data was treated as the trusted source
- CSV values were only used if API values were missing

Example rule:

```python
if api_name exists:
    use api_name
else:
    use csv_name
```

This ensured consistency and reliability in the final dataset.

### Data Cleaning Techniques Applied

All six cleaning operations were implemented:

| Cleaning Technique | Description |
|---|---|
| Null Handling | Filled or removed missing values |
| Duplicate Removal | Removed duplicate rows |
| Casing Standardization | Converted text to consistent casing |
| Type Conversion | Corrected invalid data types |
| Whitespace Removal | Stripped leading/trailing spaces |
| Outlier Handling | Removed invalid or abnormal values |

### Loading

Final cleaned dataset was loaded into:

- CSV file
- MySQL database

### Idempotency

Duplicate insertion prevention was implemented using:

- Primary keys
- `drop_duplicates()`
- SQL conflict handling

Running the pipeline multiple times does not insert duplicate rows.

---

# Task 2 — Data Quality Audit System

## Objective

Create a reporting layer on top of an ETL pipeline to detect and track data quality issues.

## Features Implemented

### Data Extraction

Fetched 100 posts from:

```text
https://jsonplaceholder.typicode.com/posts
```

### Data Quality Checks

The system automatically detected:

- Null values
- Duplicate rows
- Type mismatches
- Out-of-range values
- Inconsistent string formatting

### Transformations and Enrichments

Implemented:

- Word count columns
- Title casing
- Filtering invalid rows
- Ranking logic

Example engineered columns:

```python
title_word_count
body_word_count
rank
```

### Audit Reporting

Generated structured reports containing:

- Issue type
- Count before cleaning
- Count after cleaning
- Number of fixes applied
- Before/after row counts

Reports were exported as:

- CSV audit report
- Formatted console table

### Database Loading

Cleaned data was loaded into MySQL successfully.

---

# Task 3 — Modular Logged ETL Capstone

## Objective

Design a production-style ETL system with reusable modular functions and logging.

## ETL Architecture

The pipeline was divided into four reusable functions:

```python
extract()
clean()
transform()
load()
```

Each function can be independently:

- Tested
- Reused
- Debugged
- Extended

---

# Logging System

Extensive logging was implemented throughout the pipeline.

Each stage logs:

- Current operation
- Number of input rows
- Number of output rows
- Errors and warnings

Example:

```python
[INFO] Extracting API data...
[INFO] 100 rows extracted
[INFO] Cleaning completed
[INFO] 95 rows remaining after duplicate removal
```

---

# Feature Engineering

Three or more calculated columns were created.

Examples:

- Word count
- Score category
- Pass/fail indicator
- Rank
- Completion rate

---

# GroupBy Analysis

Used `groupby()` to generate summary statistics:

- Mean
- Minimum
- Maximum

Example:

```python
df.groupby("category")["score"].agg(["mean", "min", "max"])
```

---

# SQLAlchemy Integration

## What is SQLAlchemy?

SQLAlchemy is a powerful Python SQL toolkit and ORM (Object Relational Mapper) used for interacting with databases efficiently.

Official Website:

- [SQLAlchemy Official Documentation](https://www.sqlalchemy.org?utm_source=chatgpt.com)

## Why SQLAlchemy Was Used

SQLAlchemy simplified:

- MySQL connections
- Database operations
- Table creation
- Data insertion
- Idempotent loading

Instead of writing raw SQL queries manually, Pandas integrates directly with SQLAlchemy using:

```python
df.to_sql()
```

---

# MySQL Connection Example

```python
from sqlalchemy import create_engine

engine = create_engine(
    "mysql+pymysql://username:password@localhost/database_name"
)
```

---

# Loading Data Using SQLAlchemy

```python
df.to_sql(
    name="clean_posts",
    con=engine,
    if_exists="append",
    index=False
)
```

---

# Key Concepts Learned

## ETL Fundamentals

- Extracting data from APIs
- Reading local CSV files
- Building reusable pipelines

## Data Cleaning

- Handling null values
- Removing duplicates
- Standardizing data formats
- Detecting outliers

## Data Transformation

- Feature engineering
- Ranking and categorization
- Aggregations and summaries

## API Handling

- Timeouts
- Retries
- Status code validation
- Exception handling

## Database Engineering

- Connecting Python with MySQL
- Using SQLAlchemy
- Preventing duplicate inserts
- Idempotent loading strategies

## Data Quality Engineering

- Audit reporting
- Tracking fixes
- Measuring dataset quality

## Software Engineering Practices

- Modular coding
- Logging
- Reusable functions
- Maintainable ETL architecture

---

# Future Improvements

Possible enhancements:

- Airflow scheduling
- Docker containerization
- Cloud database integration
- Incremental loading
- Automated testing
- CI/CD integration
- Data validation frameworks

---

# Conclusion

This project demonstrates the practical implementation of real-world ETL engineering concepts including:

- Fault-tolerant extraction
- Data quality auditing
- Modular pipeline architecture
- SQLAlchemy database integration
- Idempotent MySQL loading
- Production-style logging and transformation

The project helped strengthen core data engineering skills and provided hands-on experience with scalable ETL system design.
