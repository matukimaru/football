import json
import logging
import os
import random
from datetime import datetime

from utils import extract_data

HEADERS = [
    "Fixture",  # 0
    "Date",
    "Home Team",
    "Away Team",
    "Hm",
    "Dr",  # 5
    "Aw",
    "Hm1H",
    "Dr1H",
    "Aw1H",
    "Ov",  # 10
    "Un",
    "BtY",
    "BtN",
    "Prd",
    "Sts",  # 15
    "GlHm",
    "GlAw",
    "Res",  # 18
]


class Analyze:
    def __init__(self, _dates: list) -> None:
        # custom logger
        logging.basicConfig(
            level=logging.INFO,
            format="%(asctime)s - %(name)s - %(levelname)s : %(message)s",
        )

        # init dates. _dates should be provided with the correct format (YYYY-MM-DD)
        self.date_format = "%Y-%m-%d"
        self.dates = _dates

        # init weeks
        self.weeks = [
            datetime.strptime(d, self.date_format).isocalendar().week
            for d in self.dates
        ]

        # list of interesting fixtures
        self._interesting = {}
        self._counts = {
            "over_25": {"pass": 0, "fail": 0, "pending": 0},
            "under_25": {"pass": 0, "fail": 0, "pending": 0},
            "match_winner": {
                "home": {"pass": 0, "fail": 0},
                "away": {"pass": 0, "fail": 0},
                "draw": 0,
                "pending": 0,
            },
        }

        self._data = []

        for idx, date in enumerate(self.dates):
            # check if the files exist
            if os.path.exists(f"outputs/week-{self.weeks[idx]}/fixtures/{date}.json"):
                if os.path.exists(f"outputs/week-{self.weeks[idx]}/odds/{date}.json"):
                    if os.path.exists(
                        f"outputs/week-{self.weeks[idx]}/predictions/{date}.json"
                    ):
                        # open files
                        with open(
                            f"outputs/week-{self.weeks[idx]}/fixtures/{date}.json", "r"
                        ) as f:
                            fixtures = json.loads(f.read())
                        with open(
                            f"outputs/week-{self.weeks[idx]}/odds/{date}.json", "r"
                        ) as f:
                            odds = json.loads(f.read())
                        with open(
                            f"outputs/week-{self.weeks[idx]}/predictions/{date}.json",
                            "r",
                        ) as f:
                            predictions = json.loads(f.read())

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

                            # process fixture
                            self.data.append(
                                process_fixture(fixture, odd, prediction, {})
                            )

                            # # extract key indicators
                            # self.data.append(extract_data(fixture, odd, prediction))

                    else:
                        logging.error(f"predictions file for {date} does not exist")
                        exit(0)
                else:
                    logging.error(f"odds file for {date} does not exist")
                    exit(0)
            else:
                logging.error(f"fixtures file for {date} does not exist")
                exit(0)

        self._betslips = extract_betslips(self._data)

    @property
    def data(self):
        return self._data

    @property
    def counts(self):
        return self._counts

    @property
    def betslips(self):
        return self._betslips


def process_fixture(fixture: dict, odds: dict, prediction: dict, params={}) -> list:
    """
    This function will process a single fixture.

    Returns the suggested prediction.

    Use parameters to influence results.

    Args:
        fixture (dict): fixture data
        odds (dict): odds data
        prediction (dict): prediction data
        params (dict): optional parameters
    """
    response = [
        fixture["fixture"]["id"],
        fixture["fixture"]["date"],
        fixture["teams"]["home"]["name"],
        fixture["teams"]["away"]["name"],
    ]

    extracts = {
        1: ["Home", "Draw", "Away"],  # Match Winner
        13: ["Home", "Draw", "Away"],  # First Half Winner
        5: ["Over 2.5", "Under 2.5"],  # Over/Under 2.5
        8: ["Yes", "No"],  # BTTS
    }

    for k, v in extracts.items():
        for i in v:
            response.append(extract_avg_odd(odds, k, i))

    prd = extract_prediction(prediction)
    response.append(prd)

    response += extract_outcome(fixture, prd)

    return response


def extract_avg_odd(odds: dict, id: int, value: str) -> float:
    """
    This function will calculate the average odd.

    Args:
        odds (dict): odds data
        id (int): odd id
        value (str): odd value (e.g. "Home")

    Returns:
        float: average odd
    """
    average = 0.0

    try:
        outcomes = [
            float(i["odd"])
            for bookmaker in odds["bookmakers"]
            for bet in bookmaker["bets"]
            if bet["id"] == id
            for i in bet["values"]
            if i["value"] == value
        ]
        average = round(sum(outcomes) / len(outcomes), 2)
    except Exception:
        average = 0.0

    return average


def extract_prediction(prediction: dict) -> str:
    """
    This function will extract the prediction.

    Args:
        prediction (dict): prediction data

    Returns:
        srt: winner
    """
    try:
        if (
            prediction["predictions"]["winner"]["id"]
            == prediction["teams"]["home"]["id"]
        ):
            winner = "1"
        elif (
            prediction["predictions"]["winner"]["id"]
            == prediction["teams"]["away"]["id"]
        ):
            winner = "2"
        else:
            pass

        if "draw" in prediction["predictions"]["winner"]["comment"].lower():
            winner += "X"

    except Exception:
        winner = "--"

    return winner


def extract_outcome(fixture: dict, prediction: str) -> list:
    """
    This function will extract the outcome.

    Args:
        fixture (dict): fixture data
        prediction (str): prediction

    Returns:
        list: results
    """
    results = []

    status = fixture["fixture"]["status"]["short"]
    gls_hm = fixture["score"]["fulltime"]["home"]
    gls_aw = fixture["score"]["fulltime"]["away"]

    results.append(status)
    results.append(gls_hm)
    results.append(gls_aw)

    if status == "FT" or status == "PEN" or status == "AET":
        if prediction == "1X":
            try:
                if int(gls_hm) >= int(gls_aw):
                    results.append("Won")
                else:
                    results.append("Lost")
            except Exception:
                results.append("N/A")
        elif prediction == "2X":
            try:
                if int(gls_aw) >= int(gls_hm):
                    results.append("Won")
                else:
                    results.append("Lost")
            except Exception:
                results.append("N/A")
        else:
            results.append("N/A")
    else:
        results.append(status)

    return results


def extract_betslips(data: list) -> None:
    """

    Args:
        data (list): fixture data
    """
    dt = [d[0] for d in data if 0 not in d and "--" not in d]

    return betslip_chunks(dt, 30)


def betslip_chunks(l: list, n: int) -> list:
    random.shuffle(l)

    return [l[i : i + n] for i in range(0, len(l), n)]
