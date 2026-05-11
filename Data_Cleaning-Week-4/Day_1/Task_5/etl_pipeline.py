from urllib import request, parse
from urllib.error import HTTPError, URLError
import json
import os
from dotenv import load_dotenv
import pandas as pd

# BASE URL
BASE_URL = "https://api.openbrewerydb.org/v1/breweries"


# EXTRACT
def extract_data(api_url):
    # Fetch data from Open Brewery API

    print("Fetching data from API...")

    try:
        # Open API connection
        response = request.urlopen(api_url)

        # Read and decode response
        data = response.read().decode("utf-8")

        # Convert JSON string into Python object
        breweries = json.loads(data)

        # Check if data exists
        if not breweries:
            print("No data found from API")
            return None

        print(f"Total breweries fetched: {len(breweries)}")

        return breweries

    except HTTPError as e:
        print(f"[HTTP ERROR] Status Code: {e.code}")

    except URLError as e:
        print(f"[URL ERROR] Reason: {e.reason}")

    except json.JSONDecodeError:
        print("[JSON ERROR] Failed to decode JSON response")

    except Exception as e:
        print(f"[UNEXPECTED ERROR] {e}")

    return None


# SAVE RAW / MESSY DATA
def save_raw_data(breweries, filename="messy_breweries.csv"):
    # Save raw API data into CSV file

    try:
        # Convert JSON data into DataFrame
        df = pd.DataFrame(breweries)

        # CREATE MESSY DATA FOR ETL PRACTICE

        # Add duplicate rows
        df = pd.concat([df, df.iloc[:3]], ignore_index=True)

        # Add missing values
        df.loc[1, "name"] = None
        df.loc[2, "city"] = None
        df.loc[4, "state"] = None

        # Add extra spaces
        df["name"] = df["name"].astype(str) + "   "

        # Change datatype intentionally
        if "postal_code" in df.columns:
            df.loc[5, "postal_code"] = "UNKNOWN"

        # Save messy data
        df.to_csv(filename, index=False)

        print(f"[SUCCESS] Raw messy data saved to '{filename}'")
        print(f"[INFO] Total messy rows saved: {len(df)}")

    except Exception as e:
        print(f"[ERROR] Failed to save raw data: {e}")


# TRANSFORM / CLEAN DATA
def transform_data(input_file="messy_breweries.csv",
                   output_file="clean_breweries.csv"):

    # Clean and transform data

    try:
        # Load CSV file
        df = pd.read_csv(input_file)

        print(f"Rows before cleaning: {len(df)}")

        # Remove completely empty rows
        df.dropna(how="all", inplace=True)

        # HANDLE MISSING VALUES
        df.fillna({
            "name": "Unknown Brewery",
            "city": "Unknown City",
            "state": "Unknown State",
            "brewery_type": "Unknown Type"
        }, inplace=True)

        # REMOVE DUPLICATES
        before_duplicates = len(df)

        if "id" in df.columns:
            df.drop_duplicates(subset=["id"], inplace=True)

        after_duplicates = len(df)

        print(f"Duplicate rows removed: "
              f"{before_duplicates - after_duplicates}")

        # CLEAN STRING COLUMNS

        str_cols = df.select_dtypes(include="object").columns

        for col in str_cols:
            df[col] = df[col].astype(str).str.strip()

        # FIX DATATYPES
        if "postal_code" in df.columns:
            df["postal_code"] = (
                df["postal_code"]
                .astype(str)
                .str.extract(r'(\d+)')[0]
            )

        # ENRICHED / CALCULATED COLUMNS
        # Brewery name length
        df["name_length"] = df["name"].str.len()

        # State + City column
        df["location"] = df["city"] + ", " + df["state"]

        # Check if brewery has website
        if "website_url" in df.columns:
            df["has_website"] = df["website_url"].notna()

        # Brewery category
        if "brewery_type" in df.columns:
            df["is_micro_brewery"] = (
                df["brewery_type"]
                .str.lower()
                .eq("micro")
            )

        # FINAL ROW COUNT
        print(f"Rows after cleaning: {len(df)}")

        # Save cleaned data
        df.to_csv(output_file, index=False)

        print(f"[SUCCESS] Clean data saved to '{output_file}'")

        return df

    except FileNotFoundError:
        print("[ERROR] Input file not found")

    except pd.errors.EmptyDataError:
        print("[ERROR] CSV file is empty")

    except Exception as e:
        print(f"[ERROR] Transformation failed: {e}")

    return None


# MAIN PIPELINE
def main():

    print("========== ETL PIPELINE STARTED ==========")

    # Step 1: Extract data from API
    breweries = extract_data(BASE_URL)

    # Stop pipeline if extraction fails
    if not breweries:
        print("Extraction failed")
        return

    # Step 2: Save raw messy data
    save_raw_data(breweries)

    # Step 3: Transform and clean data
    cleaned_df = transform_data()

    # Check transformation result
    if cleaned_df is not None:
        print("ETL PIPELINE COMPLETED")

    else:
        print("Transformation failed")


# RUN PROGRAM
if __name__ == "__main__":
    main()