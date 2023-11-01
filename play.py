import json
import logging
import os
from datetime import datetime

from fuzzywuzzy import fuzz
from tabulate import tabulate

from analyze import strategies
from present.utils import extract_data, headers

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s : %(message)s",
)

date_format = "%Y-%m-%d"
dates = [
    "2023-10-25",
    "2023-10-26",
    "2023-10-27",
]
weeks = [datetime.strptime(date, date_format).isocalendar().week for date in dates]

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
                # flist
                with open(f"resources/flist.txt", "r") as f:
                    flist_raw = f.readlines()
                flist = [f.strip().lower() for f in flist_raw]

                #
                for fl in flist:
                    # loop through fixtures
                    for fixture in fixtures:
                        fn = f'{(fixture["teams"]["home"]["name"]).lower()} v {(fixture["teams"]["away"]["name"]).lower()}'

                        if fuzz.token_sort_ratio(fl, fn) > 85:
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

# match winner home
# response = strategies.match_winner_away(data)
print(tabulate(data, headers=headers, showindex="always", tablefmt="simple"))
# print(response[1])
