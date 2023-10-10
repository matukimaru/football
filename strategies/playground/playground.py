import json
from datetime import date

from apitools import calculate_match_winner_odds

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

count = 0

for odd in odds:
    match_winner = calculate_match_winner_odds(odd)

    # condition 1
    # if 1.95 <= home_avg <= 2.15 or 1.95 <= draw_avg <= 2.15 or 1.95 <= away_avg <= 2.15:
    #     count += 1
    #     print(f"{home_avg} : {draw_avg} : {away_avg}")

    # condition 2
    if (match_winner[0] >= 2.2 and match_winner[2] >= 2.2) and (
        abs(match_winner[0] - match_winner[2]) <= 0.2
    ):
        count += 1
        print(f"{match_winner[0]} : {match_winner[1]} : {match_winner[2]}")

    # print(f"{home_avg} : {draw_avg} : {away_avg}")
    # break

print(count)
