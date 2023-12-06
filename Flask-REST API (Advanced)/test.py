import requests

BASE = "http://127.0.0.1:5000/"

data = [{"name": "Naruto", "price": 1000, "views": 2000},
        {"name": "Sasuke", "price": 1000, "views": 2000},
        {"name": "Sakura", "price": 1000, "views": 2000},
        {"name": "Kakashi Sensei", "price": 1000, "views": 2000}]

for i in range(len(data)):
    response = requests.put(BASE + "art/" + str(i), json = data[i])
    print(response.json())

input()
response = requests.get(BASE + "art/1")
print(response.json())

response = requests.get(BASE + "art/16")
print(response.json())

response = requests.delete(BASE + "art/1")
print(response)
print("Artwork deleted.")

response = requests.get(BASE + "art/0")
print(response.json())

response = requests.get(BASE + "art/1")
print(response.json())

