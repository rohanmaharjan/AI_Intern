'''
Use the Open-Meteo weather API (free, no key needed) to fetch 7-day weather forecast for Kathmandu.
Save to CSV.
Find the hottest and coldest day.
'''
# corrected errors
'''
1. removed loop over weather_data because it is a dictionary, not a list.
2. write dates and temps as lists instead of row-by-row data.
3. used exception handling
'''

import urllib.request
import urllib.parse
import json
import csv

url = "https://api.open-meteo.com/v1/forecast"

params = {
    "latitude": 27.75,
    "longitude": 85.375,
    "daily": "temperature_2m_max",
    "timezone": "auto"
}

# Encode parameters into URL
query_string = urllib.parse.urlencode(params)
full_url = f"{url}?{query_string}"

try:
    # API request using urllib
    with urllib.request.urlopen(full_url) as response:
        data = response.read().decode("utf-8")
        weather_data = json.loads(data)

    # Extract data
    dates = weather_data["daily"]["time"]
    temps = weather_data["daily"]["temperature_2m_max"]

    # Write CSV
    try:
        with open("weather.csv", "w", newline="") as file:
            writer = csv.DictWriter(file, fieldnames=["Date", "Temperature"])
            writer.writeheader()

            for i in range(len(dates)):
                writer.writerow({
                    "Date": dates[i],
                    "Temperature": temps[i]
                })
    except IOError as e:
        print("Error writing CSV file:", e)

    # Analysis
    max_temp = max(temps)
    min_temp = min(temps)

    hottest_day = dates[temps.index(max_temp)]
    coldest_day = dates[temps.index(min_temp)]

    print(f"Hottest Day: {hottest_day} = {max_temp} °C")
    print(f"Coldest Day: {coldest_day} = {min_temp} °C")

    # Write summary
    try:
        with open("summary.txt", "w") as file:
            file.write("7-Day Weather Summary for Kathmandu\n")
            file.write(f"Hottest Day: {hottest_day} = {max_temp} °C\n")
            file.write(f"Coldest Day: {coldest_day} = {min_temp} °C\n")
    except IOError as e:
        print("Error writing summary file:", e)


except Exception as e:
    print("Unexpected error:", e)