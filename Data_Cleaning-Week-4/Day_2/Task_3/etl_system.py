import pandas as pd
from urllib import request, error
import json
from sqlalchemy import create_engine, text
from sqlalchemy.exc import SQLAlchemyError
import time
from dotenv import load_dotenv
import os
from urllib.parse import quote_plus


# LOAD ENVIRONEMNET VARIABLES
load_dotenv()

# DATABASE CONFIGURATION
MYSQL_USER = "root"
MYSQL_PASSWORD = quote_plus(os.getenv("password"))
MYSQL_HOST = "localhost"
MYSQL_PORT = "3306"
MYSQL_DATABASE = "etl_capstone"

# SQLAlchemy Connection URL
DATABASE_URL = (
    f"mysql+pymysql://{MYSQL_USER}:{MYSQL_PASSWORD}"
    f"@{MYSQL_HOST}:{MYSQL_PORT}/{MYSQL_DATABASE}"
)

# Create Engine
engine = create_engine(DATABASE_URL)

# EXTRACT FUNCTION to extract from public api
def extract(api_url):
    print("\n[EXTRACT] Starting extraction process...")

    try:
        start_time = time.time()

        # Send request with timeout
        response = request.urlopen(api_url, timeout=10)

        # Status code check
        if response.status != 200:
            print(f"[EXTRACT] Failed with status code: {response.status}")
            return pd.DataFrame()

        # Read and decode response
        data = response.read().decode("utf-8")

        # Convert JSON to Python object
        json_data = json.loads(data)

        # Convert to DataFrame
        df = pd.DataFrame(json_data)

        end_time = time.time()

        print(f"[EXTRACT] Successfully extracted data")
        print(f"[EXTRACT] Rows extracted: {len(df)}")
        print(f"[EXTRACT] Time taken: {round(end_time - start_time, 2)} seconds")

        return df

    except error.HTTPError as e:
        print(f"[EXTRACT] HTTP Error: {e}")

    except error.URLError as e:
        print(f"[EXTRACT] URL Error: {e}")

    except Exception as e:
        print(f"[EXTRACT] Unexpected Error: {e}")

    return pd.DataFrame()


# CLEAN FUNCTION
def clean(df):
    print("\n[CLEAN] Starting cleaning process...")

    try:
        input_rows = len(df)
        print(f"[CLEAN] Input rows: {input_rows}")

        # Remove duplicates
        df = df.drop_duplicates()

        # Remove null titles or bodies
        df = df.dropna(subset=["title", "body"])

        # Strip spaces
        df["title"] = df["title"].str.strip()
        df["body"] = df["body"].str.strip()

        # Reset index
        df = df.reset_index(drop=True)

        output_rows = len(df)

        print(f"[CLEAN] Output rows: {output_rows}")
        print(f"[CLEAN] Removed rows: {input_rows - output_rows}")

        return df

    except Exception as e:
        print(f"[CLEAN] Error during cleaning: {e}")
        return pd.DataFrame()


# TRANSFORM FUNCTION, transforms and enrich data
def transform(df):
    print("\n[TRANSFORM] Starting transformation process...")

    try:

        input_rows = len(df)
        print(f"[TRANSFORM] Input rows: {input_rows}")

        # Title Word Count
        df["title_word_count"] = df["title"].apply(
            lambda x: len(str(x).split())
        )

        # Body Word Count
        df["body_word_count"] = df["body"].apply(
            lambda x: len(str(x).split())
        )

        # Total Content Length
        df["total_content_length"] = (
            df["title"].str.len() + df["body"].str.len()
        )

        # Score Category
        df["score_category"] = df["body_word_count"].apply(
            lambda x: (
                "Short"
                if x < 20
                else "Medium"
                if x < 40
                else "Long"
            )
        )

        # Engagement Score
        df["engagement_score"] = (
            df["title_word_count"] * 2
            + df["body_word_count"]
        )

        # GROUPBY SUMMARY
        print("\n[TRANSFORM] GroupBy Summary Table")

        summary = df.groupby("score_category").agg({
            "body_word_count": ["mean", "min", "max"],
            "engagement_score": ["mean", "min", "max"]
        })

        print(summary)

        output_rows = len(df)

        print(f"\n[TRANSFORM] Output rows: {output_rows}")

        return df

    except Exception as e:
        print(f"[TRANSFORM] Error during transformation: {e}")
        return pd.DataFrame()


# LOAD FUNCTION
def load(df, csv_filename, table_name):
    print("\n[LOAD] Starting loading process...")

    try:

        input_rows = len(df)
        print(f"[LOAD] Input rows: {input_rows}")

        # LOAD TO CSV
        df.to_csv(csv_filename, index=False)

        print(f"[LOAD] CSV saved successfully: {csv_filename}")

        # IDEMPOTENCY HANDLING
        df = df.drop_duplicates(subset=["id"])

        # LOAD TO MYSQL
        with engine.begin() as conn:
            # Create table if not exists
            create_table_query = f"""
            CREATE TABLE IF NOT EXISTS {table_name} (
                id BIGINT PRIMARY KEY,
                userId BIGINT,
                title TEXT,
                body TEXT,
                title_word_count INT,
                body_word_count INT,
                total_content_length INT,
                score_category VARCHAR(50),
                engagement_score INT
            )
            """

            conn.execute(text(create_table_query))

            # Delete existing ids to avoid duplicates
            existing_ids = tuple(df["id"].tolist())

            if len(existing_ids) > 0:

                delete_query = text(
                    f"DELETE FROM {table_name} WHERE id IN :ids"
                )

                conn.execute(
                    delete_query,
                    {"ids": existing_ids}
                )

        # Insert fresh data
        df.to_sql(
            name=table_name,
            con=engine,
            if_exists="append",
            index=False
        )

        print(f"[LOAD] Data loaded into MySQL table: {table_name}")
        print(f"[LOAD] Output rows loaded: {len(df)}")

    except SQLAlchemyError as e:
        print(f"[LOAD] Database Error: {e}")

    except Exception as e:
        print(f"[LOAD] Unexpected Error: {e}")


# MAIN PIPELINE
def main():

    print("\nETL PIPELINE STARTED")

    API_URL = "https://jsonplaceholder.typicode.com/posts"

    # Extract
    extracted_df = extract(API_URL)

    if extracted_df.empty:
        print("\nPipeline stopped: Extraction failed")
        return

    # Clean
    cleaned_df = clean(extracted_df)

    if cleaned_df.empty:
        print("\nPipeline stopped: Cleaning failed")
        return

    # Transform
    transformed_df = transform(cleaned_df)

    if transformed_df.empty:
        print("\nPipeline stopped: Transformation failed")
        return

    # Load
    load(transformed_df, csv_filename="enriched_posts.csv", table_name="enriched_posts")

    print("\nETL PIPELINE COMPLETED")


# RUN PIPELINE
if __name__ == "__main__":
    main()