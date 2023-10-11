import json
from datetime import datetime

from tabulate import tabulate

import analyze.utils as analyzer
from collect.collector import Collect

# collect
dates = ["2023-10-10", "2023-10-11"]
collector = Collect(dates)

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

print(tabulate(data, headers=analyzer.headers, showindex="always", tablefmt="simple"))
