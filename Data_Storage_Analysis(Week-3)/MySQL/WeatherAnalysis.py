'''
Goal Use the Open-Meteo API to fetch 7-day weather for 3 cities and store + compare them in MySQL.
1 Fetch 7-day forecast (max + min temp) for 3 cities of your choice using Open-Meteo API
2 Create weather.db with a forecasts table: id, city, date, max_temp, min_temp
3 Insert all 21 rows (3 cities × 7 days) into the database
4 Query 1: Which city has the highest average max temperature?
5 Query 2: Find the single hottest day across all 3 cities
6 Query 3: Find days where the temperature difference (max - min) is greater than 10°C
7 Save a summary report to a summary.txt file using Python file handling (Week 1 skill!)
Deliverable:weather.db+summary.txt+scriptshowingall3queryoutputs·Bonus:addhumiditydataasa4thcolumn
'''
import requests
import mysql.connector
from dotenv import load_dotenv
import os

# Load environment variables
load_dotenv()

# MySQL Connection
conn = mysql.connector.connect(
    host="localhost",
    user="root",
    password=os.getenv("Database_Password")
)

cursor = conn.cursor()

# Create database if not exists
cursor.execute("CREATE DATABASE IF NOT EXISTS weather")
cursor.execute("USE weather")

# drop old table
cursor.execute("DROP TABLE IF EXISTS forecasts")

# create table forecasts
cursor.execute("""
CREATE TABLE IF NOT EXISTS forecasts (
    id INT AUTO_INCREMENT PRIMARY KEY,
    city VARCHAR(100),
    date DATE,
    max_temp FLOAT,
    min_temp FLOAT,
    humidity FLOAT,
    UNIQUE KEY unique_city_date (city, date) # unique as one city should have only one forcast per date
)
""")

# 3 Cities
cities = {
    "Lalitpur": {"lat": 27.6667, "lon": 85.3167},
    "Sarlahi": {"lat": 26.9689, "lon": 85.5684},
    "Humla": {"lat": 29.9667, "lon": 81.8333}
}

# Fetch 7-day forecast from Open-Meteo
for city, location in cities.items():

    url = ("https://api.open-meteo.com/v1/forecast")

    params = {
        "latitude": {location['lat']},
        "longitude": {location['lon']},
        "daily": [
            "temperature_2m_max", 
            "temperature_2m_min", 
            "relative_humidity_2m_mean"
        ],
        "timezone": "auto",
        "forecast_days": 7 
    }
    
    try:
        response = requests.get(url, params=params)
        response.raise_for_status()
        data = response.json()

        dates = data["daily"]["time"]
        max_temps = data["daily"]["temperature_2m_max"]
        min_temps = data["daily"]["temperature_2m_min"]
        humidity_values = data["daily"]["relative_humidity_2m_mean"]

        print(f"{city} weather data fetched successfully!")

        for i in range(7):
            insert_query = """
            INSERT INTO forecasts
            (city, date, max_temp, min_temp, humidity)
            VALUES (%s, %s, %s, %s, %s)
            ON DUPLICATE KEY UPDATE
            max_temp = VALUES(max_temp),
            min_temp = VALUES(min_temp),
            humidity = VALUES(humidity)
            """

            cursor.execute(insert_query, (
                city,
                dates[i],
                max_temps[i],
                min_temps[i],
                humidity_values[i]
            ))

        conn.commit()

    except Exception as e:
        print(f"Error fetching data for {city}: {e}")

# QUERY 1 - Which city has highest average max temp?
print("\n--- Query 1: Highest Average Max Temperature ---")

cursor.execute("""
SELECT city, AVG(max_temp) AS avg_max_temp
FROM forecasts
GROUP BY city
ORDER BY avg_max_temp DESC
LIMIT 1
""")

result1 = cursor.fetchone()

print(
    f"City: {result1[0]}, "
    f"Average Max Temperature: {result1[1]:.2f}°C"
)

# QUERY 2 - Find single hottest day across all cities
print("\n--- Query 2: Single Hottest Day ---")

cursor.execute("""
SELECT city, date, max_temp
FROM forecasts
ORDER BY max_temp DESC
LIMIT 1
""")

result2 = cursor.fetchone()

print(
    f"City: {result2[0]}, "
    f"Date: {result2[1]}, "
    f"Max Temp: {result2[2]}°C"
)

# QUERY 3 - Days where (max - min) > 10°C
print("\n--- Query 3: Days with Temp Difference > 10°C ---")

cursor.execute("""
SELECT city, date, max_temp, min_temp,
(max_temp - min_temp) AS difference
FROM forecasts
WHERE (max_temp - min_temp) > 10
ORDER BY difference DESC
""")

result3 = cursor.fetchall()

for row in result3:
    print(f"City: {row[0]}, Date: {row[1]}, Max: {row[2]}°C, Min: {row[3]}°C, Difference: {row[4]:.2f}°C")


# Save summary report to summary.txt
with open("summary.txt", "w", encoding="utf-8") as file:
    file.write("WEEKLY WEATHER SUMMARY REPORT\n\n")

    file.write("Query 1: Highest Average Max Temperature\n")
    file.write(f"City: {result1[0]}, Average Max Temperature: {result1[1]:.2f}°C\n\n")

    file.write("Query 2: Single Hottest Day\n")
    file.write(f"City: {result2[0]}, Date: {result2[1]}, Max Temp: {result2[2]}°C\n\n")

    file.write("Query 3: Days with Temp Difference > 10°C\n")

    for row in result3:
        file.write(f"City: {row[0]}, Date: {row[1]}, Max: {row[2]}°C, Min: {row[3]}°C, Difference: {row[4]:.2f}°C\n")

print("\nsummary.txt file created successfully!")

# Close connection

#for delete purpose
# cursor.execute("DELETE FROM forecasts")
# conn.commit()

cursor.close()
conn.close()

print("\nWeather API --> MySQL Task Completed Successfully!")
