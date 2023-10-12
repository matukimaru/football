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
        #
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
                logging.info(f"created output directories for week {w}")
        # init ApiSports
        self.api = ApiSports()

        # execute collection
        self.collect_fixtures()
        self.collect_odds()

    def collect_fixtures(self):
        for idx, date in enumerate(self.dates):
            params = {"date": date.strftime("%Y-%m-%d"), "timezone": "Africa/Nairobi"}
            logging.info(f"fetching fixtures for {date.strftime('%Y-%m-%d')}...")
            response = self.api.query("/fixtures", params)
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
                params = {
                    "date": date.strftime("%Y-%m-%d"),
                    "timezone": "Africa/Nairobi",
                }
                logging.info(
                    f"fetching (page 1) odds for {date.strftime('%Y-%m-%d')}..."
                )
                response = self.api.query("/odds", params)
                if not len(response["errors"]):
                    pages = response["paging"]["total"]
                    odds += response["response"]
                    logging.info(f"extra pages to fetch = {pages - 1}")
                    if pages > 1:
                        for page in range(pages - 1):
                            # throttling requests
                            if (page + 1) % 8 == 0:
                                print("sleeping")
                                sleep(61)

                            params = {
                                "date": date.strftime("%Y-%m-%d"),
                                "timezone": "Africa/Nairobi",
                                "page": page + 2,
                            }
                            logging.info(
                                f"fetching (page {page + 2}) odds for {date.strftime('%Y-%m-%d')}..."
                            )
                            response = self.api.query("/odds", params)
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

    # //todo prepend fixture-id to predictions
    def collect_prediction(self, fixture, date):
        name = (
            f"{fixture['teams']['home']['name']} vs {fixture['teams']['away']['name']}"
        )
        if not os.path.exists(
            f"outputs/week-{date.isocalendar().week}/predictions/{date.strftime('%Y-%m-%d')}.json"
        ):
            # file does not exist - create and update
            params = {
                "fixture": fixture["fixture"]["id"],
            }
            logging.info(f"fetching prediction for {name}")
            response = self.api.query("/predictions", params)
            if not len(response["errors"]):
                # write to file
                with open(
                    f"outputs/week-{date.isocalendar().week}/predictions/{date.strftime('%Y-%m-%d')}.json",
                    "w+",
                ) as f:
                    f.write(json.dumps(response["response"]))
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
                predictions = json.loads(f.read())

            # loop through predictions and check if fixture's prediction is there
            exists = False
            for prediction in predictions:
                n = f"{prediction['teams']['home']['name']} vs {prediction['teams']['away']['name']}"
                if n == name:
                    exists = True
                    break
                else:
                    continue
            if not exists:
                # fetch prediction
                logging.info(f"fetching prediction for {name}")
                response = self.api.query("/predictions", params)
                if not len(response["errors"]):
                    # update predictions list
                    predictions.append(response["response"][0])
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
