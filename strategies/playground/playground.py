import json
from datetime import date

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
    home = [
        float(i["odd"])
        for bookmaker in odd["bookmakers"]
        for bet in bookmaker["bets"]
        if bet["id"] == 1
        for i in bet["values"]
        if i["value"] == "Home"
    ]
    home_avg = round(sum(home) / len(home), 2)

    draw = [
        float(i["odd"])
        for bookmaker in odd["bookmakers"]
        for bet in bookmaker["bets"]
        if bet["id"] == 1
        for i in bet["values"]
        if i["value"] == "Draw"
    ]
    draw_avg = round(sum(draw) / len(draw), 2)

    away = [
        float(i["odd"])
        for bookmaker in odd["bookmakers"]
        for bet in bookmaker["bets"]
        if bet["id"] == 1
        for i in bet["values"]
        if i["value"] == "Away"
    ]
    away_avg = round(sum(away) / len(away), 2)

    # condition 1
    # if 1.95 <= home_avg <= 2.15 or 1.95 <= draw_avg <= 2.15 or 1.95 <= away_avg <= 2.15:
    #     count += 1
    #     print(f"{home_avg} : {draw_avg} : {away_avg}")

    # condition 2
    if (home_avg >= 2.2 and away_avg >= 2.2) and (abs(home_avg - away_avg) <= 0.2):
        count += 1
        print(f"{home_avg} : {draw_avg} : {away_avg}")

    # print(f"{home_avg} : {draw_avg} : {away_avg}")
    # break

print(count)
