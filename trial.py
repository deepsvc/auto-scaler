import requests
import json

response = requests.get(
    'http://localhost:8123/app/status', headers={
        "Accept": "application/json",
    })

res = response.json()["cpu"]["highPriority"]
# res = response.text

print(res)


data = {"replicas": 10}


response = requests.put(
    'http://localhost:8123/app/replicas', json=data, headers={
        "Content-Type": "application/json",
    })

# res = response.json()["response"]
res = response.text

print(res)