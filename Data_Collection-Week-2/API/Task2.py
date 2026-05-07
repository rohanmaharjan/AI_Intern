'''
Fetch posts from the API.
Save them to a CSV with columns: id, title, body.
Then read the CSV back and print only posts where title contains more than 5 words.
'''
# corrected fields
'''
1. fixed issue where file was read but never used
2. exception handling
'''
import urllib.request
import json
import csv

url = "https://jsonplaceholder.typicode.com/posts/"

try:
    # API request using urllib
    with urllib.request.urlopen(url) as response:
        data = response.read().decode("utf-8")
        posts = json.loads(data)

    # write csv
    with open("posts.csv", "w", newline="") as file:
            writer = csv.DictWriter(file, fieldnames=["id", "title", "body"])
            writer.writeheader()

            for post in posts:
                writer.writerow({"id": post["id"], "title": post["title"], "body": post["body"]})

    with open("posts.csv", "r") as file:
         reader = csv.DictReader(file)
         for row in reader:
            words = row["title"].split()
            if len(words)>5:
                print(f'Id: {row["id"]} \t\t Title: {row["title"]} \t\t Body: {row["body"]}')
        

except Exception as e:
    print("Unexpected error:", e)