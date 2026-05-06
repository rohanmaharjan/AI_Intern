'''
Use the JSONPlaceholder API to fetch a list of users. Print each user's name, email and city to the termianl.
'''

import requests

url = "https://jsonplaceholder.typicode.com/users"

response = requests.get(url)

# print(response.status_code)

if response.status_code == 200:
    users = response.json()

    # print("name     email   city")

    for user in users:
        # print(user["name"],"  |  ", user["email"],"  |  ", user["address"]["city"])
        print(f'Name: {user["name"]} \t\t Email: {user["email"]} \t\t City: {user["address"]["city"]}')

