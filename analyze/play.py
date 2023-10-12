import json
import logging

from tabulate import tabulate

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s : %(message)s",
)

with open("resources/predictions.json", "r") as f:
    predictions = json.loads(f.read())
print(len(predictions))

headers = [  # 18
    "Winner",
    "G-Home",
    "G-Away",
    "P-Hm",
    "P-Dr",
    "P-Aw",
    "F-Hm",
    "F-Aw",
    "At-Hm",
    "At-Aw",
    "Df-Hm",
    "Df-Aw",
    "GF-Hm",
    "GA-Hm",
    "GF-Aw",
    "GA-Aw",
    "LG-Hm",
    "LG-Aw",
]

display = []

for prediction in predictions:
    hold = []
    winner = prediction["predictions"]["winner"]["name"]
    hold.append(winner)
    goals = [
        prediction["predictions"]["goals"]["home"],
        prediction["predictions"]["goals"]["away"],
    ]
    hold += goals
    percent = [
        prediction["predictions"]["percent"]["home"],
        prediction["predictions"]["percent"]["draw"],
        prediction["predictions"]["percent"]["away"],
    ]
    hold += percent
    meta = {
        "form": [
            prediction["teams"]["home"]["last_5"]["form"],
            prediction["teams"]["away"]["last_5"]["form"],
        ],
        "attack": [
            prediction["teams"]["home"]["last_5"]["att"],
            prediction["teams"]["away"]["last_5"]["att"],
        ],
        "defence": [
            prediction["teams"]["home"]["last_5"]["def"],
            prediction["teams"]["away"]["last_5"]["def"],
        ],
        "goals": {
            "for": [
                prediction["teams"]["home"]["last_5"]["goals"]["for"]["total"],
                prediction["teams"]["away"]["last_5"]["goals"]["for"]["total"],
            ],
            "against": [
                prediction["teams"]["home"]["last_5"]["goals"]["against"]["total"],
                prediction["teams"]["away"]["last_5"]["goals"]["against"]["total"],
            ],
        },
        "league": [
            prediction["teams"]["home"]["league"]["form"],
            prediction["teams"]["away"]["league"]["form"],
        ],
    }
    hold += meta["form"]
    hold += meta["attack"]
    hold += meta["defence"]
    hold.append(meta["goals"]["for"][0])
    hold.append(meta["goals"]["against"][0])
    hold.append(meta["goals"]["for"][1])
    hold.append(meta["goals"]["against"][1])
    hold += meta["league"]

    display.append(hold)

    # logging.info(f"winner: {winner}\ngoals: {goals}\npercent: {percent}\nmeta: {meta}")

    # break

print(tabulate(display, headers=headers, showindex="always", tablefmt="simple"))
