import json
from datetime import date

from tabulate import tabulate

from helpers.utils.odds import calculate_match_winner_odds

# from decouple import config

# root_path = config("ROOT_PATH")

today = date.today()
week = date.today().isocalendar().week

with open(f"outputs/week-{week}/fixtures/{today}.json", "r") as f:
    fixtures = json.loads(f.read())
print(len(fixtures))

with open(f"outputs/week-{week}/odds/{today}.json", "r") as f:
    odds = json.loads(f.read())
print(len(odds))


# for fixture in fixtures:
#     _id = fixture["fixture"]["id"]

#     for odd in odds:
#         if _id == odd["fixture"]["id"]:
#             with open(f"strategies/playground/odd.json", "w+") as f:
#                 f.write(json.dumps(odd))
#             break

# display
data = [
    [
        "Fixture",
        "Home",
        "Draw",
        "Away",
        "Over 2.5",
        "Under 2.5",
        "Status",
        "Home Goals",
        "Away Goals",
    ]
]

count = 0

for odd in odds:
    match_winner = calculate_match_winner_odds(odd)
    # append outcome
    match_winner += [
        [
            fixture["fixture"]["status"]["short"],
            fixture["goals"]["home"],
            fixture["goals"]["away"],
        ]
        for fixture in fixtures
        if fixture["fixture"]["id"] == odd["fixture"]["id"]
    ][0]
    data.append(match_winner)

    # condition 1
    # if (
    #     1.95 <= match_winner[0] <= 2.15
    #     or 1.95 <= match_winner[1] <= 2.15
    #     or 1.95 <= match_winner[2] <= 2.15
    # ):
    #     count += 1
    #     print(f"{match_winner[0]} : {match_winner[1]} : {match_winner[2]}")

    # # condition 2
    # if (match_winner[0] >= 2.2 and match_winner[2] >= 2.2) and (
    #     abs(match_winner[0] - match_winner[2]) <= 0.2
    # ):
    #     count += 1
    #     print(f"{match_winner[0]} : {match_winner[1]} : {match_winner[2]}")


print(tabulate(data, headers="firstrow", showindex="always", tablefmt="simple"))
