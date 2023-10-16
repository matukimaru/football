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
    "2023-10-16",
]
weeks = [datetime.strptime(date, date_format).isocalendar().week for date in dates]

# collect data
collector = Collect(dates)

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
                    data.append(extract_data(fixture, odd, prediction))

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
print(tabulate(data, headers=headers, showindex="always", tablefmt="simple"))
