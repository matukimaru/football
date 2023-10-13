# import json
# import logging
# from time import sleep

# from apiutils import ApiSports

# logging.basicConfig(
#     level=logging.INFO,
#     format="%(asctime)s - %(name)s - %(levelname)s : %(message)s",
# )

# api = ApiSports()

# with open("outputs/week-41/fixtures/2023-10-12.json", "r") as f:
#     fixtures = json.loads(f.read())

# predictions = []

# count = 0
# for fixture in fixtures:
#     params = {"fixture": fixture["fixture"]["id"]}
#     response = api.query("/predictions", params)
#     count += 1
#     if not len(response["errors"]):
#         predictions.append(response["response"][0])
#         logging.info(
#             f"{fixture['teams']['home']['name']} vs {fixture['teams']['away']['name']}"
#         )
#         if count % 10 == 0:
#             logging.info(f"sleeping for a minute")
#             sleep(61)
#     else:
#         logging.error(f"{response['errors']}")

# with open("resources/predictions.json", "w+") as f:
#     f.write(json.dumps(predictions))


# import json

# # fresh = [{"id": "1", "name": "John"}, {"id": "2", "name": "Jane"}]


# with open("resources/test.json", "r") as f:
#     curr = json.loads(f.read())

# another = [{"id": "10", "name": "XXIC"}]
# curr += [another[0]]

# with open("resources/test.json", "w") as f:
#     f.write(json.dumps(curr))

# site = {
#     "Website": "DigitalOcean",
#     # "Tutorial": "How To Add to a Python Dictionary",
#     # "Author": "Sammy",
# }

# guests = {"Guest1": "Dino Sammy", "Guest2": "Xray Sammy"}

# new_site = site | guests

# print("site: ", site)
# print("guests: ", guests)
# print("new_site: ", new_site)


import json

data = {
    "employees": [
        {"name": "John Doe", "department": "Marketing", "place": "Remote"},
        {"name": "Jane Doe", "department": "Software Engineering", "place": "Remote"},
        {"name": "Don Joe", "department": "Software Engineering", "place": "Office"},
    ]
}

# .dumps() as a string
json_string = json.dumps(data)

print(type(data))  # type dict
print(type(json_string))  # type str

loaded_json = json.loads(json_string)
print(type(loaded_json))  # type dict
