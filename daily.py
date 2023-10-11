import json
import logging
import os
from datetime import date, timedelta
from time import sleep

from apitools import API

api = API()
today = date.today() - timedelta(days=1)
week = today.isocalendar().week

# create folder structure
if not os.path.exists(f"outputs/week-{week}"):
    os.mkdir(f"outputs/week-{week}")
    os.mkdir(f"outputs/week-{week}/fixtures")
    os.mkdir(f"outputs/week-{week}/odds")
    os.mkdir(f"outputs/week-{week}/predictions")
    os.mkdir(f"outputs/week-{week}/logs")

logging.basicConfig(
    filename=f"outputs/week-{week}/logs/{today}.log",
    encoding="utf-8",
    format="%(asctime)s %(message)s",
    level=logging.DEBUG,
)


def fixtures():
    params = {
        "date": today,
        "timezone": "Africa/Nairobi",
    }
    logging.info(f"fetching fixtures for {today}")

    response = api.query("/fixtures", params)
    if not len(response["errors"]):
        with open(f"outputs/week-{week}/fixtures/{today}.json", "w+") as f:
            f.write(json.dumps(response["response"]))
    else:
        logging.info(f"error fetching fixtures for {today}")
        logging.debug(response)


def odds():
    odds = []

    params = {
        "date": today,
        "timezone": "Africa/Nairobi",
    }
    logging.info(f"fetching (page 1) odds for {today}")

    # fetch first page
    response = api.query("/odds", params)
    if not len(response["errors"]):
        pages = response["paging"]["total"]
        odds += response["response"]

        # loop through pages
        print(f"Pages = {pages}")
        if pages > 1:
            for page in range(pages - 1):
                # throttling requests
                if (page + 1) % 9 == 0:
                    print("sleeping")
                    sleep(61)

                params = {
                    "date": today,
                    "timezone": "Africa/Nairobi",
                    "page": page + 2,
                }
                logging.info(f"fetching (page {page + 2}) odds for {today}")

                response = api.query("/odds", params)
                if not len(response["errors"]):
                    odds += response["response"]
                else:
                    logging.info(f"error fetching odds (page {page + 2})")
                    logging.debug(response)

    else:
        logging.info(f"error fetching odds")
        logging.debug(response)

    with open(f"outputs/week-{week}/odds/{today}.json", "w+") as f:
        f.write(json.dumps(odds))


# fetch fixtures
fixtures()

# fetch odds only if they have not been fetched before
if not os.path.exists(f"outputs/week-{week}/odds/{today}.json"):
    odds()
