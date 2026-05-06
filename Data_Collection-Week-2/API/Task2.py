'''
Fetch posts from the API.
Save them to a CSV with columns: id, title, body.
Then read the CSV back and print only posts where title contains more than 5 words.
'''

import requests
import csv

url = "https://jsonplaceholder.typicode.com/posts/"
response = requests.get(url)

if response.status_code == 200:
    posts = response.json()

    with open("posts.csv", "w", newline="") as file:
        writer = csv.DictWriter(file, fieldnames=["id", "title", "body"])
        writer.writeheader()


        for post in posts:
            writer.writerow({"id": post["id"], "title": post["title"], "body": post["body"]})

with open("posts.csv", "r") as file:
    for post in posts:

        title = post["title"]
        words = title.split()
        if len(words)>5:
            print(f'Id: {post["id"]} \t\t Title: {post["title"]} \t\t Body: {post["body"]}')

