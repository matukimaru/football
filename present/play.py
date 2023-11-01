import json
import logging
import os
from datetime import datetime

from tabulate import tabulate

from analyze import strategies
from collect.collector import Collect
from present.utils import extract_data, headers

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s : %(message)s",
)

date_format = "%Y-%m-%d"
dates = [
    "2023-10-26",
    "2023-10-27",
    "2023-10-28",
    "2023-10-29",
    "2023-10-30",
]
weeks = [datetime.strptime(date, date_format).isocalendar().week for date in dates]

# collect data
# collector = Collect(dates)

# display data
data = []

for idx, date in enumerate(dates):
    # check if the files exist
    if os.path.exists(f"outputs/week-{weeks[idx]}/fixtures/{date}.json"):
        if os.path.exists(f"outputs/week-{weeks[idx]}/odds/{date}.json"):
            if os.path.exists(f"outputs/week-{weeks[idx]}/predictions/{date}.json"):
                # open files
                with open(f"outputs/week-{weeks[idx]}/fixtures/{date}.json", "r") as f:
                    fixtures = json.loads(f.read())
                with open(f"outputs/week-{weeks[idx]}/odds/{date}.json", "r") as f:
                    odds = json.loads(f.read())
                with open(
                    f"outputs/week-{weeks[idx]}/predictions/{date}.json", "r"
                ) as f:
                    predictions = json.loads(f.read())

                # loop through fixtures
                for fixture in fixtures:
                    # get odd
                    try:
                        odd = [
                            odd
                            for odd in odds
                            if odd["fixture"]["id"] == fixture["fixture"]["id"]
                        ][0]
                    except IndexError:
                        odd = {}
                    # get prediction
                    try:
                        prediction = [
                            prediction
                            for prediction in predictions
                            if prediction["fixture"] == fixture["fixture"]["id"]
                        ][0]
                    except IndexError:
                        prediction = {}

                    # get info and append to display data
                    # logging.info(fixture)
                    data.append(extract_data(fixture, odd, prediction))
                    # //todo extract only for fixtures in a predefined list

            else:
                logging.error(f"predictions file for {date} does not exist")
                exit(0)
        else:
            logging.error(f"odds file for {date} does not exist")
            exit(0)
    else:
        logging.error(f"fixtures file for {date} does not exist")
        exit(0)

# display data
# print(tabulate(data, headers=headers, showindex="always", tablefmt="simple"))

#
# correct score first half
# print("\nCorrect score first half\n")
# response = strategies.correct_score_first_half(data)
# with open(
#     f"outputs/week-{weeks[idx]}/strategies/{date}_correct_score_first_half.json", "w+"
# ) as f:
#     f.write(json.dumps(response[0]))
# print(tabulate(response[0], headers=headers, showindex="always", tablefmt="simple"))


# # both teams to score
# print("\nBoth teams to score\n")
# response = strategies.both_teams_to_score(data)
# with open(
#     f"outputs/week-{weeks[idx]}/strategies/{date}_both_teams_to_score.json", "w+"
# ) as f:
#     f.write(json.dumps(response[0]))
# print(tabulate(response[0], headers=headers, showindex="always", tablefmt="simple"))


# # match winner
# response = strategies.match_winner(data)
# counts = response[1]
# msg = f"""\n
# Fixtures: {counts["evaluated"]}
#     Home predicted to win:
#     - Evaluated: {counts["home"]["evaluated"]} -> {counts["home"]["evaluated"]*100/counts["evaluated"]:.2f}%
#     - Wins: {counts["home"]["wins"]} -> {counts["home"]["wins"]*100/(counts["home"]["wins"] + counts["home"]["losses"]):.2f}%
#     - Losses: {counts["home"]["losses"]} -> {counts["home"]["losses"]*100/(counts["home"]["wins"] + counts["home"]["losses"]):.2f}%
#     Away predicted to win:
#     - Evaluated: {counts["away"]["evaluated"]} -> {counts["away"]["evaluated"]*100/counts["evaluated"]:.2f}%
#     - Wins: {counts["away"]["wins"]} -> {counts["away"]["wins"]*100/(counts["away"]["wins"] + counts["away"]["losses"]):.2f}%
#     - Losses: {counts["away"]["losses"]} -> {counts["away"]["losses"]*100/(counts["away"]["wins"] + counts["away"]["losses"]):.2f}%
# Draws: {counts["draws"]} -> {counts["draws"]*100/counts["evaluated"]:.2f}%
# """
# print(
#     tabulate(response[0], headers=headers[:-2], showindex="always", tablefmt="simple")
# )
# print(msg)

# match winner home
response = strategies.match_winner_away(data)
print(
    tabulate(response[0], headers=headers[:-2], showindex="always", tablefmt="simple")
)
print(response[1])
