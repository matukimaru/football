import json
import logging
import os
from datetime import datetime
from time import sleep

from collect.apiutils import ApiSports


class Collect:
    def __init__(self, _dates: list) -> None:
        # custom logger
        logging.basicConfig(
            level=logging.INFO,
            format="%(asctime)s - %(name)s - %(levelname)s : %(message)s",
        )
        # init dates. _dates should be provided with the correct format (YYYY-MM-DD)
        self.date_format = "%Y-%m-%d"
        self.dates = []
        for d in _dates:
            self.dates.append(datetime.strptime(d, self.date_format))
        # init weeks
        self.weeks = []
        for d in self.dates:
            self.weeks.append(d.isocalendar().week)
        # init output directories
        for w in self.weeks:
            if not os.path.exists(f"outputs/week-{w}"):
                os.mkdir(f"outputs/week-{w}")
                os.mkdir(f"outputs/week-{w}/fixtures")
                os.mkdir(f"outputs/week-{w}/odds")
                os.mkdir(f"outputs/week-{w}/predictions")
                os.mkdir(f"outputs/week-{w}/logs")
                os.mkdir(f"outputs/week-{w}/strategies")
                logging.info(f"created output directories for week {w}")
        # init ApiSports
        self.api = ApiSports()
        # api call counter
        self.count = 1

        # execute collection
        self.collect_odds()  # collecting odds first as collecting fixtures also collects predictions
        self.collect_fixtures()

    def rate_limit(self):
        # if self.count % 10 == 0:
        #     logging.info(f"\n>>> rate limiting... sleep for a minute\n")
        #     sleep(61)
        pass

    def collect_fixtures(self):
        for idx, date in enumerate(self.dates):
            self.rate_limit()
            params = {"date": date.strftime("%Y-%m-%d"), "timezone": "Africa/Nairobi"}
            logging.info(f"fetching fixtures for {date.strftime('%Y-%m-%d')}...")
            response = self.api.query("/fixtures", params)
            self.count += 1
            if not len(response["errors"]):
                fixtures = response["response"]
                with open(
                    f"outputs/week-{self.weeks[idx]}/fixtures/{date.strftime('%Y-%m-%d')}.json",
                    "w+",
                ) as f:
                    f.write(json.dumps(fixtures))
                logging.info(
                    f"successfully collected {len(response['response'])} fixtures for {date.strftime('%Y-%m-%d')}."
                )
                # collect predictions
                for fixture in fixtures:
                    self.collect_prediction(fixture, date)
            else:
                logging.error(
                    f"failed to collect fixtures for date {date.strftime('%Y-%m-%d')}... {response['errors']}"
                )

    def collect_odds(self):
        for idx, date in enumerate(self.dates):
            # execute only if odds have not been fetched before
            if not os.path.exists(
                f"outputs/week-{self.weeks[idx]}/odds/{date.strftime('%Y-%m-%d')}.json"
            ):
                odds = []
                self.rate_limit()
                params = {
                    "date": date.strftime("%Y-%m-%d"),
                    "timezone": "Africa/Nairobi",
                }
                logging.info(
                    f"fetching (page 1) odds for {date.strftime('%Y-%m-%d')}..."
                )
                response = self.api.query("/odds", params)
                self.count += 1
                if not len(response["errors"]):
                    pages = response["paging"]["total"]
                    odds += response["response"]
                    logging.info(f"extra pages to fetch = {pages - 1}")
                    if pages > 1:
                        for page in range(pages - 1):
                            self.rate_limit()
                            params = {
                                "date": date.strftime("%Y-%m-%d"),
                                "timezone": "Africa/Nairobi",
                                "page": page + 2,
                            }
                            logging.info(
                                f"fetching (page {page + 2}) odds for {date.strftime('%Y-%m-%d')}..."
                            )
                            response = self.api.query("/odds", params)
                            self.count += 1
                            if not len(response["errors"]):
                                odds += response["response"]
                                logging.info(f"successful")
                            else:
                                logging.error(
                                    f"failed... (page {page + 2})... {response['errors']}"
                                )
                with open(
                    f"outputs/week-{self.weeks[idx]}/odds/{date.strftime('%Y-%m-%d')}.json",
                    "w+",
                ) as f:
                    f.write(json.dumps(odds))
                logging.info(
                    f"successfully fetched odds for {date.strftime('%Y-%m-%d')}"
                )
            else:
                logging.info(f"odds for {date.strftime('%Y-%m-%d')} already exist")

    def collect_prediction(self, fixture, date):
        prepend = {
            "fixture": fixture["fixture"]["id"],
        }
        name = (
            f"{fixture['teams']['home']['name']} vs {fixture['teams']['away']['name']}"
        )
        if not os.path.exists(
            f"outputs/week-{date.isocalendar().week}/predictions/{date.strftime('%Y-%m-%d')}.json"
        ):
            self.rate_limit()
            # file does not exist - create and update
            params = {
                "fixture": fixture["fixture"]["id"],
            }
            logging.info(f"fetching prediction for {name}")
            response = self.api.query("/predictions", params)
            self.count += 1
            if not len(response["errors"]):
                # write to file
                with open(
                    f"outputs/week-{date.isocalendar().week}/predictions/{date.strftime('%Y-%m-%d')}.json",
                    "w+",
                ) as f:
                    f.write(
                        json.dumps(
                            [prepend | response["response"][0]],
                        )
                    )
                logging.info("file created and updated")
            else:
                logging.error(f"no prediction for {name}: {response['errors']}")
        else:
            # file exists - open, check, and update if fixture's prediction is not there
            params = {
                "fixture": fixture["fixture"]["id"],
            }

            # get current predictions
            with open(
                f"outputs/week-{date.isocalendar().week}/predictions/{date.strftime('%Y-%m-%d')}.json",
                "r",
            ) as f:
                try:
                    predictions = json.loads(f.read())
                    # exit(0)
                except Exception:
                    predictions = []

            # loop through predictions and check if fixture's prediction is there
            exists = False
            for prediction in predictions:
                try:
                    n = f"{prediction['teams']['home']['name']} vs {prediction['teams']['away']['name']}"
                    if n == name:
                        exists = True
                        break
                    else:
                        continue
                except Exception:
                    continue
            if not exists:
                # fetch prediction
                self.rate_limit()
                logging.info(f"fetching prediction for {name}")
                response = self.api.query("/predictions", params)
                self.count += 1
                if not len(response["errors"]):
                    # update predictions list
                    predictions.append(prepend | response["response"][0])
                else:
                    logging.error(f"no prediction for {name}: {response['errors']}")
            else:
                logging.info(f"prediction for {name} already exists")

            # save predictions to file
            with open(
                f"outputs/week-{date.isocalendar().week}/predictions/{date.strftime('%Y-%m-%d')}.json",
                "w",
            ) as f:
                f.write(json.dumps(predictions))
                logging.info(f"file updated with prediction for {name}")
