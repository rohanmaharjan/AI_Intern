'''
Use the Open-Meteo weather API (free, no key needed) to fetch 7-day weather forecast for Kathmandu.
Save to CSV.
Find the hottest and coldest day.
'''

import requests
import csv

url = "https://api.open-meteo.com/v1/forecast"

params = {
    "latitude": 27.75,
    "longitude": 85.375,
    "daily": "temperature_2m_max"
}


response = requests.get(url, params=params)

if response.status_code == 200:
    weather_data = response.json()

with open("weather.csv", "w", newline="") as file:
    writer = csv.DictWriter(file, fieldnames=["Date", "Temperature"])
    writer.writeheader()

    for weather in weather_data:
        dates = weather_data["daily"]["time"]
        temps = weather_data["daily"]["temperature_2m_max"]
    writer.writerow({"Date": dates, "Temperature": temps})

max_temp = max(temps)
min_temp = min(temps)

hottest_day = dates[temps.index(max_temp)]
coldest_day = dates[temps.index(min_temp)]

print(f"Hottest Day: {hottest_day} = {max_temp} C")
print(f"Coldest Day: {coldest_day} = {min_temp} C")

with open("summary.txt", "w") as file:
    file.write("7-Day Weather Summary for Kathmandu\n")
    file.write(f"Hottest Day: {hottest_day} = {max_temp} C\n")
    file.write(f"Coldest Day: {coldest_day} = {min_temp} C\n")

