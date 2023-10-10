import json

from apitools import API

api = API()

params = {}
response = api.query("/odds/bets", params)
if not len(response["errors"]):
    with open("resources/json/markets.json", "w+") as f:
        f.write(json.dumps(response["response"]))
else:
    print(response)
