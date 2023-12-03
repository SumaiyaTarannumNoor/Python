import requests

BASE = "http://127.0.0.1:5000/"

data = [{"name": "Naruto", "likes": 1000, "views": 2000},
        {"name": "Sasuke", "likes": 1000, "views": 2000},
        {"name": "Sakura", "likes": 1000, "views": 2000},
        {"name": "Kakashi Sensei", "likes": 1000, "views": 2000}]

for i in range(len(data)):
    response = requests.put(BASE + "video/" + str(i), json = data[i])
    print(response.json())

input()
response = requests.delete(BASE + "video/1")
#print(response)
print("Video deleted.")
input()
response = requests.get(BASE + "video/1")
print(response.json())
