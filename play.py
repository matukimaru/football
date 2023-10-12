import json
import math
from datetime import datetime

from tabulate import tabulate

import analyze.utils as analyzer

# collect
dates = [
    "2023-10-12",
]

# analyze
data = []
date_format = "%Y-%m-%d"
for d in dates:
    # load collected data
    today = datetime.strptime(d, date_format)
    week = today.isocalendar().week
    with open(
        f"outputs/week-{week}/fixtures/{today.strftime('%Y-%m-%d')}.json", "r"
    ) as f:
        fixtures = json.loads(f.read())
    with open(f"outputs/week-{week}/odds/{today.strftime('%Y-%m-%d')}.json", "r") as f:
        odds = json.loads(f.read())

    # calculate status
    for fixture in fixtures:
        for odd in odds:
            if fixture["fixture"]["id"] == odd["fixture"]["id"]:
                data.append(analyzer.calculate_status(fixture, odd))
                # move to next fixture
                break

# strategies
# loop through fixtures
hold = []
counts = [0, 0, 0, 0, 0, 0, 0]
for entry in data:
    # consider completed fixtures only
    if entry[11] == "FT" or entry[11] == "PEN":
        counts[0] += 1
        # check if home team won
        if entry[14] > entry[15]:
            counts[2] += 1
            if (entry[14] + entry[15]) >= 3:
                counts[5] += 1
            if 1.6 <= entry[1] <= 2.1:
                counts[6] += 1
        # check if away team won
        if entry[14] < entry[15]:
            counts[3] += 1
        # check if it was a draw
        if entry[14] == entry[15]:
            counts[4] += 1
    else:
        counts[1] += 1

print(
    f"analyzed {counts[0]} of {len(data)} fixtures. ({counts[1]}) not considered\n"
    f"- {counts[2]} are Home wins : {math.ceil(counts[2] / counts[0] * 100)}%\n"
    f"  - {counts[5]} are 3+ goals : {math.ceil(counts[5] / counts[2] * 100)}%\n"
    f"  - {counts[6]} are within 1.9 - 2.1 adds : {math.ceil(counts[6] / counts[2] * 100)}%\n"
    f"- {counts[3]} are Away wins : {math.ceil(counts[3] / counts[0] * 100)}%\n"
    f"- {counts[4]} are Draws : {math.ceil(counts[4] / counts[0] * 100)}%\n"
)

# print(tabulate(hold, headers=analyzer.headers, showindex="always", tablefmt="simple"))
