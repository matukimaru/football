import json

with open("resources/json/markets.json", "r") as f:
    markets = json.loads(f.read())

for i in markets:
    print(i)
