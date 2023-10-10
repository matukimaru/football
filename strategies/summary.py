import json
from datetime import date, timedelta

from tabulate import tabulate

from helpers.utils.odds import calculate_averages


def daily(date: date, week: int):
    # get raw data
    with open(f"outputs/week-{week}/fixtures/{date}.json", "r") as f:
        fixtures = json.loads(f.read())
    with open(f"outputs/week-{week}/odds/{date}.json", "r") as f:
        odds = json.loads(f.read())

    # build data and header
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
        ],
    ]

    # get data per fixture
    for odd in odds:
        # get average odds for interesting markets
        averages = calculate_averages(odd)
        # get fixture outcomes
        outcomes = [
            [
                fixture["fixture"]["status"]["short"],
                fixture["goals"]["home"],
                fixture["goals"]["away"],
            ]
            for fixture in fixtures
            if fixture["fixture"]["id"] == odd["fixture"]["id"]
        ][0]
        data.append((averages + outcomes))

    return data


# test daily() summary function
data = daily(date.today() - timedelta(days=1), 41)
print(tabulate(data, headers="firstrow", showindex="always", tablefmt="simple"))
