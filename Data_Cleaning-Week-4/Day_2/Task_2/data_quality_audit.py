import pandas as pd
import json
from urllib import request
from urllib.error import URLError, HTTPError
from sqlalchemy import create_engine
from sqlalchemy.exc import SQLAlchemyError
from dotenv import load_dotenv
import os
import pymysql
from urllib.parse import quote_plus

# load environmennt variables
load_dotenv()

# api link
API_URL = "https://jsonplaceholder.typicode.com/posts"

DB_USER = 'root'
DB_PASSWORD = quote_plus(os.getenv("password"))
DB_HOST = 'localhost'
DB_PORT = 3306
DB_NAME = 'quality_audit_db'
TABLE_NAME = 'clean_posts'


# fetch data from api
def fetch_data(api_url):

    try:
        print("Fetching data from API...")

        response = request.urlopen(api_url, timeout=10)

        data = response.read()

        posts = json.loads(data)

        df = pd.DataFrame(posts)

        print("Data fetched successfully")
        print(f"Total Rows Fetched: {len(df)}")

        return df

    except HTTPError as e:
        print("HTTP Error:", e)

    except URLError as e:
        print("URL Error:", e)

    except Exception as e:
        print("Unexpected Error:", e)


# create dirty data for testing audit system
def create_dirty_data(df):

    # create duplicate rows
    df = pd.concat([df, df.iloc[:2]], ignore_index=True)

    # create null values
    df.loc[5, 'title'] = None
    df.loc[10, 'body'] = None

    # inconsistent string formats
    df.loc[3, 'title'] = 'HELLO WORLD'
    df.loc[4, 'title'] = 'python programming'

    # out of range value
    df.loc[7, 'userId'] = -10

    # type mismatch
    df.loc[8, 'userId'] = 'abc'

    return df


# generate audit report before cleaning
def audit_data(df):

    print("\nData Quality Check")

    report = {
        'Issue': [],
        'Count Before Cleaning': [],
        'Count Fixed': []
    }

    # null values
    null_counts = df.isnull().sum()

    for column, count in null_counts.items():

        if count > 0:

            report['Issue'].append(f'Null Values in {column}')
            report['Count Before Cleaning'].append(int(count))
            report['Count Fixed'].append(0)

    # duplicate rows
    duplicate_count = df.duplicated().sum()

    report['Issue'].append('Duplicate Rows')
    report['Count Before Cleaning'].append(int(duplicate_count))
    report['Count Fixed'].append(0)

    # type mismatch
    invalid_type_count = 0

    for value in df['userId']:

        try:
            int(value)

        except:
            invalid_type_count += 1

    report['Issue'].append('Type Mismatch in userId')
    report['Count Before Cleaning'].append(invalid_type_count)
    report['Count Fixed'].append(0)

    # out of range values
    numeric_userid = pd.to_numeric(df['userId'], errors='coerce')

    out_of_range_count = (numeric_userid <= 0).sum()

    report['Issue'].append('Out of Range userId')
    report['Count Before Cleaning'].append(int(out_of_range_count))
    report['Count Fixed'].append(0)

    # inconsistent title formats
    inconsistent_titles = 0

    for title in df['title'].dropna():

        if title != str(title).title():
            inconsistent_titles += 1

    report['Issue'].append('Inconsistent Title Format')
    report['Count Before Cleaning'].append(inconsistent_titles)
    report['Count Fixed'].append(0)

    return report, inconsistent_titles


# clean and transform data
def clean_data(df, report, inconsistent_titles):

    print("\nCleaning Data")

    before_rows = len(df)

    # remove duplicates
    before_dup = len(df)

    df = df.drop_duplicates()

    removed_duplicates = before_dup - len(df)

    report['Count Fixed'][1] = removed_duplicates

    # handle null values
    null_before = df.isnull().sum().sum()

    df['title'] = df['title'].fillna('Unknown Title')

    df['body'] = df['body'].fillna('No Content')

    null_after = df.isnull().sum().sum()

    fixed_nulls = int(null_before - null_after)

    for i in range(len(report['Issue'])):

        if 'Null Values' in report['Issue'][i]:
            report['Count Fixed'][i] = fixed_nulls

    # fix type mismatch
    df['userId'] = pd.to_numeric(df['userId'], errors='coerce')

    invalid_before = df['userId'].isnull().sum()

    df['userId'] = df['userId'].fillna(1)

    report['Count Fixed'][2] = int(invalid_before)

    # fix out of range values
    out_before = (df['userId'] <= 0).sum()

    df.loc[df['userId'] <= 0, 'userId'] = 1

    report['Count Fixed'][3] = int(out_before)

    # fix inconsistent string formats
    df['title'] = df['title'].str.title()

    report['Count Fixed'][4] = inconsistent_titles

    # enrichments
    print("\nApplying Enrichments")

    # word count
    df['title_word_count'] = df['title'].apply(
        lambda x: len(str(x).split())
    )

    df['body_word_count'] = df['body'].apply(
        lambda x: len(str(x).split())
    )

    # filtering
    df = df[df['userId'] <= 5]

    # ranking
    df['rank'] = df['body_word_count'].rank(
        method='dense',
        ascending=False
    )

    after_rows = len(df)

    return df, report, before_rows, after_rows


# generate final audit report
def generate_report(report, before_rows, after_rows):

    print("\nGenerating Audit Report")

    report_df = pd.DataFrame(report)

    summary_df = pd.DataFrame({
        'Metric': ['Rows Before Cleaning', 'Rows After Cleaning'],
        'Value': [before_rows, after_rows]
    })

    print("\nData Quality Report")
    print(report_df)

    print("\nRow Count Summary")
    print(summary_df)

    report_df.to_csv('audit_report.csv', index=False)

    summary_df.to_csv('row_summary.csv', index=False)

    print("\nAudit report saved successfully")


# load clean data into mysql
def load_to_mysql(df):

    print("\nLoading Data Into MySQL")

    try:

        engine = create_engine(
            f'mysql+pymysql://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}'
        )

        df.to_sql(
            TABLE_NAME,
            con=engine,
            if_exists='replace',
            index=False
        )

        print("Clean data loaded into MySQL successfully")

    except SQLAlchemyError as e:
        print("Database Error:", e)

    except Exception as e:
        print("Unexpected Error:", e)


# main function
def main():

    df = fetch_data(API_URL)

    if df is not None:

        df = create_dirty_data(df)

        report, inconsistent_titles = audit_data(df)

        df, report, before_rows, after_rows = clean_data(
            df,
            report,
            inconsistent_titles
        )

        generate_report(
            report,
            before_rows,
            after_rows
        )

        load_to_mysql(df)

        print("\nFinal Clean Data")
        print(df.head())

        print("\nETL Pipeline Completed Successfully")


# run program
if __name__ == "__main__":
    main()