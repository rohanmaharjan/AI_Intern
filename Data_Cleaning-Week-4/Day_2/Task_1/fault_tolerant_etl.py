"""
FAULT-TOLERANT MULTI-SOURCE ETL PIPELINE
=======================================

This script:
1. Extracts data from JSONPlaceholder API with retries and timeout handling
2. Reads messy CSV data
3. Normalizes nested JSON using pd.json_normalize()
4. Merges datasets with conflict resolution
5. Applies multiple data cleaning techniques
6. Loads cleaned data into MySQL
7. Exports cleaned data to CSV

Author: Rohan Maharjan
"""

# IMPORT LIBRARIES
import requests
import pandas as pd
import numpy as np
import time
import io
import os
import dotenv
import pymysql

from urllib.parse import quote_plus
from sqlalchemy import create_engine, text
from sqlalchemy.types import (
    String,
    BigInteger,
    Integer,
    Text
)

# LOAD ENVIRONMENT VARIABLES
dotenv.load_dotenv()

# CONFIGURATION
USERS_URL = "https://jsonplaceholder.typicode.com/users"
POSTS_URL = "https://jsonplaceholder.typicode.com/posts"

OUTPUT_CSV = "cleaned_unified_data.csv"

MYSQL_USER = "root"
MYSQL_PASSWORD = quote_plus(os.getenv("password"))
MYSQL_HOST = "localhost"
MYSQL_PORT = 3306
MYSQL_DATABASE = "etl_pipe_db"

TABLE_NAME = "merged_data"

# API EXTRACTION FUNCTIONS
def fetch_data_with_retries(url, retries=3, delay=5):
    """
    Fetch data from API with retry mechanism.
    """

    for attempt in range(retries):

        try:
            response = requests.get(url, timeout=10)

            # Raise HTTP errors (4xx / 5xx)
            response.raise_for_status()

            print(f"Successfully fetched data from: {url}")

            return response.json()

        except requests.exceptions.Timeout:
            print(f"Timeout error for {url} | Retry {attempt + 1}/{retries}")

        except requests.exceptions.ConnectionError as e:
            print(f"Connection error for {url}: {e}")

        except requests.exceptions.HTTPError as e:
            print(f"HTTP error for {url}: {e}")

        except Exception as e:
            print(f"Unexpected error for {url}: {e}")

        time.sleep(delay)

    print(f"Failed to fetch data from {url}")

    return None


def extract_users_data():
    """
    Extract and normalize users data.
    """

    users_data = fetch_data_with_retries(USERS_URL)

    if users_data:
        users_df = pd.json_normalize(users_data)

        print("\nUsers Data Extracted Successfully")
        print(users_df.head())

        return users_df

    return pd.DataFrame()


def extract_posts_data():
    """
    Extract posts data.
    """

    posts_data = fetch_data_with_retries(POSTS_URL)

    if posts_data:
        posts_df = pd.DataFrame(posts_data)

        print("\nPosts Data Extracted Successfully")
        print(posts_df.head())

        return posts_df

    return pd.DataFrame()


# CSV EXTRACTION FUNCTION
def load_messy_csv():
    """
    Load messy CSV data into DataFrame.
    """

    csv_data = """
id,Name,Email,Age,City,  Country,  Salary
1,  John Doe,john.doe@example.com,30,New York,USA,60000
2,Jane Smith  ,jane.smith@example.com, 25,  Los Angeles, USA ,75000
3,Peter Jones,peter.jones@example.com,40,London  ,UK,80000
4,  Alice Brown,alice.brown@example.com, 35,Paris  ,France,  62000
5,Bob White  ,bob.white@example.com,  50,  Berlin,Germany,  90000
6,  Charlie Green,charlie.green@example.com,,Sydney  ,Australia,
7,Diana Prince,diana.prince@example.com,28,Themyscira,USA,70000
"""

    try:
        csv_df = pd.read_csv(io.StringIO(csv_data))

        # Clean column names
        csv_df.columns = csv_df.columns.str.strip().str.lower()

        print("\nCSV Data Loaded Successfully")
        print(csv_df.head())

        return csv_df

    except Exception as e:
        print(f"Error reading CSV data: {e}")

        return pd.DataFrame()


# MERGING FUNCTION
def merge_datasets(users_df, csv_df):
    """
    Merge API and CSV datasets using email.
    """

    merged_df = pd.merge(
        users_df,
        csv_df,
        on="email",
        how="outer",
        suffixes=("_api", "_csv")
    )

    # Conflict Resolution
    # Prioritize API name over CSV name

    merged_df["name"] = merged_df["name_api"].fillna(
        merged_df["name_csv"]
    )

    merged_df.drop(
        columns=["name_api", "name_csv"],
        inplace=True
    )

    print("\nDatasets Merged Successfully")

    return merged_df


# DATA CLEANING FUNCTIONS
def handle_null_values(df):
    """
    Fill missing values.
    """

    numerical_cols = ["age", "salary"]

    categorical_cols = [
        "city",
        "country",
        "username",
        "phone",
        "website",
        "address.street",
        "address.suite",
        "address.city",
        "address.zipcode",
        "company.name",
        "company.catchPhrase",
        "company.bs",
        "name"
    ]

    # Handle numeric columns

    for col in numerical_cols:

        if col in df.columns:

            if df[col].dtype == "object":
                df[col] = df[col].replace(
                    r"^\s*$",
                    np.nan,
                    regex=True
                )

            df[col] = pd.to_numeric(
                df[col],
                errors="coerce"
            )

            median_value = df[col].median()

            df[col] = df[col].fillna(median_value)

    # Handle categorical columns

    for col in categorical_cols:

        if col in df.columns:
            df[col] = df[col].fillna("Unknown")

    return df


def remove_duplicates(df):
    """
    Remove duplicate rows.
    """

    initial_rows = len(df)

    df.drop_duplicates(inplace=True)

    removed = initial_rows - len(df)

    print(f"\nRemoved {removed} duplicate rows")

    return df


def standardize_casing(df):
    """
    Standardize text casing.
    """

    string_cols = df.select_dtypes(include=["object"]).columns

    for col in string_cols:

        if col == "email":
            df[col] = df[col].str.lower()

        elif col in [
            "name",
            "username",
            "city",
            "country",
            "address.city",
            "address.street",
            "company.name"
        ]:
            df[col] = df[col].apply(
                lambda x: x.title()
                if isinstance(x, str) and x != "Unknown"
                else x
            )

        else:
            df[col] = df[col].str.strip()

    return df


def convert_data_types(df):
    """
    Convert columns to proper data types.
    """

    numeric_columns = ["id_api", "id_csv", "age", "salary"]

    for col in numeric_columns:

        if col in df.columns:

            df[col] = pd.to_numeric(
                df[col],
                errors="coerce"
            )

            df[col] = df[col].round().astype("Int64")

    return df


def trim_whitespace(df):
    """
    Remove extra whitespace from string columns.
    """

    string_cols = df.select_dtypes(include=["object"]).columns

    for col in string_cols:

        df[col] = df[col].apply(
            lambda x: x.strip()
            if isinstance(x, str)
            else x
        )

    return df


def cap_outliers_iqr(df, column):
    """
    Cap outliers using IQR method.
    """

    numeric_series = pd.to_numeric(
        df[column],
        errors="coerce"
    )

    median_value = numeric_series.median()

    numeric_series = numeric_series.fillna(median_value)

    Q1 = numeric_series.quantile(0.25)
    Q3 = numeric_series.quantile(0.75)

    IQR = Q3 - Q1

    lower_bound = Q1 - 1.5 * IQR
    upper_bound = Q3 + 1.5 * IQR

    clipped_series = numeric_series.clip(
        lower=lower_bound,
        upper=upper_bound
    )

    df[column] = clipped_series.round().astype("Int64")

    return df


def handle_outliers(df):
    """
    Apply outlier handling.
    """

    numerical_cols = ["age", "salary"]

    for col in numerical_cols:

        if col in df.columns:
            df = cap_outliers_iqr(df, col)

    return df


def clean_data(df):
    """
    Run all cleaning steps.
    """

    print("\n========== BEFORE CLEANING ==========")
    print(df.info())

    print("\nMissing Values:")
    print(df.isnull().sum())

    df = handle_null_values(df)

    df = remove_duplicates(df)

    df = standardize_casing(df)

    df = convert_data_types(df)

    df = trim_whitespace(df)

    df = handle_outliers(df)

    print("\n========== AFTER CLEANING ==========")
    print(df.info())

    print("\nMissing Values:")
    print(df.isnull().sum())

    print("\nCleaned Data Preview:")
    print(df.head())

    return df


# CSV EXPORT FUNCTION

def export_to_csv(df, output_path):
    """
    Save DataFrame to CSV.
    """

    df.to_csv(output_path, index=False)

    print(f"\nCleaned data exported to: {output_path}")


# MYSQL FUNCTIONS
def create_mysql_engine():
    """
    Create SQLAlchemy engine.
    """

    engine = create_engine(
        f"mysql+pymysql://{MYSQL_USER}:{MYSQL_PASSWORD}@{MYSQL_HOST}:{MYSQL_PORT}/{MYSQL_DATABASE}"
    )

    return engine


def create_table(engine):
    """
    Create MySQL table if it does not exist.
    """

    create_table_sql = f"""
    CREATE TABLE IF NOT EXISTS {TABLE_NAME} (
        id_api BIGINT,
        username VARCHAR(255),
        email VARCHAR(255) PRIMARY KEY,
        phone VARCHAR(255),
        website VARCHAR(255),
        address_street VARCHAR(255),
        address_suite VARCHAR(255),
        address_city VARCHAR(255),
        address_zipcode VARCHAR(255),
        address_geo_lat VARCHAR(255),
        address_geo_lng VARCHAR(255),
        company_name VARCHAR(255),
        company_catchPhrase TEXT,
        company_bs TEXT,
        id_csv BIGINT,
        age INT,
        city VARCHAR(255),
        country VARCHAR(255),
        salary INT,
        name VARCHAR(255)
    );
    """

    with engine.connect() as connection:
        connection.execute(text(create_table_sql))
        connection.commit()

    print(f"\nTable '{TABLE_NAME}' ready")


def prepare_dataframe_for_mysql(df):
    """
    Prepare DataFrame for MySQL insertion.
    """

    df = df.copy()

    df.columns = df.columns.str.replace(".", "_", regex=False)

    df["email"] = (
        df["email"]
        .astype(str)
        .str.lower()
        .str.strip()
    )

    return df


def insert_ignore_into_mysql(df, engine):
    """
    Insert data using INSERT IGNORE.
    """

    connection = engine.raw_connection()

    cursor = connection.cursor()

    columns = ", ".join(
        [f"`{col}`" for col in df.columns]
    )

    placeholders = ", ".join(
        ["%s"] * len(df.columns)
    )

    insert_sql = f"""
    INSERT IGNORE INTO `{TABLE_NAME}`
    ({columns})
    VALUES ({placeholders})
    """

    data = [tuple(row) for row in df.values]

    try:
        cursor.executemany(insert_sql, data)

        connection.commit()

        print(
            f"\nSuccessfully inserted/ignored {len(data)} rows"
        )

    except Exception as e:

        connection.rollback()

        print(f"Error inserting data: {e}")

    finally:
        cursor.close()
        connection.close()


def load_to_mysql(df):
    """
    Complete MySQL loading pipeline.
    """

    try:
        engine = create_mysql_engine()

        with engine.connect() as connection:
            print("\nConnected to MySQL successfully")

        create_table(engine)

        df_mysql = prepare_dataframe_for_mysql(df)

        insert_ignore_into_mysql(df_mysql, engine)

    except Exception as e:
        print(f"MySQL Error: {e}")


# MAIN PIPELINE

def run_etl_pipeline():

    print("\n========== STARTING ETL PIPELINE ==========")

    # Extract
    users_df = extract_users_data()

    posts_df = extract_posts_data()

    csv_df = load_messy_csv()

    # Merge
    merged_df = merge_datasets(users_df, csv_df)

    # Clean
    cleaned_df = clean_data(merged_df)

    # Export
    export_to_csv(cleaned_df, OUTPUT_CSV)

    # Load to MySQL
    load_to_mysql(cleaned_df)

    print("\n========== ETL PIPELINE COMPLETED ==========")


# ENTRY POINT

if __name__ == "__main__":
    run_etl_pipeline()