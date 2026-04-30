import requests, csv
# import mysql.connector

url = "https://jsonplaceholder.typicode.com/users"

response = requests.get(url)

if response.status_code==200:
    users = response.json()

    with open("user.csv", "w", newline="") as file:
        writer = csv.DictWriter(file, fieldnames=["id", "name", "email", "phone", "city", "company_name"])
        writer.writeheader()


        for post in users:
            writer.writerow({"id": post["id"], "name": post["name"], "email": post["email"], "phone": post["phone"], "city": post["address"]["city"], "company_name": post["company"]["name"]})