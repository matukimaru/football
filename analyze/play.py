import json
import logging
from datetime import date, timedelta


class Analyze:
    def __init__(self, fixture: dict, odds: dict):
        logging.basicConfig(
            level=logging.INFO,
            format="%(asctime)s - %(name)s - %(levelname)s : %(message)s",
        )
        self.fixture = fixture
        self.odds = odds

    def calculate_average_odds(self) -> list:
        # if an odd does not exist, return 0
        response = []

        # Match Winner
        home = [
            float(i["odd"])
            for bookmaker in self.odds["bookmakers"]
            for bet in bookmaker["bets"]
            if bet["id"] == 1
            for i in bet["values"]
            if i["value"] == "Home"
        ]
        home_avg = round(sum(home) / len(home), 2)
        response.append(home_avg)
        #
        draw = [
            float(i["odd"])
            for bookmaker in self.odds["bookmakers"]
            for bet in bookmaker["bets"]
            if bet["id"] == 1
            for i in bet["values"]
            if i["value"] == "Draw"
        ]
        draw_avg = round(sum(draw) / len(draw), 2)
        response.append(draw_avg)
        #
        away = [
            float(i["odd"])
            for bookmaker in self.odds["bookmakers"]
            for bet in bookmaker["bets"]
            if bet["id"] == 1
            for i in bet["values"]
            if i["value"] == "Away"
        ]
        away_avg = round(sum(away) / len(away), 2)
        response.append(away_avg)

        # First Half Winner
        home_fh = [
            float(i["odd"])
            for bookmaker in self.odds["bookmakers"]
            for bet in bookmaker["bets"]
            if bet["id"] == 13
            for i in bet["values"]
            if i["value"] == "Home"
        ]
        home_fh_avg = round(sum(home_fh) / len(home_fh), 2)
        response.append(home_fh_avg)
        #
        draw_fh = [
            float(i["odd"])
            for bookmaker in self.odds["bookmakers"]
            for bet in bookmaker["bets"]
            if bet["id"] == 13
            for i in bet["values"]
            if i["value"] == "Draw"
        ]
        draw_fh_avg = round(sum(draw_fh) / len(draw_fh), 2)
        response.append(draw_fh_avg)
        #
        away_fh = [
            float(i["odd"])
            for bookmaker in self.odds["bookmakers"]
            for bet in bookmaker["bets"]
            if bet["id"] == 13
            for i in bet["values"]
            if i["value"] == "Away"
        ]
        away_fh_avg = round(sum(away_fh) / len(away_fh), 2)
        response.append(away_fh_avg)

        # Over/Under 2.5
        over25 = []
        try:
            over25 = [
                float(i["odd"])
                for bookmaker in self.odds["bookmakers"]
                for bet in bookmaker["bets"]
                if bet["id"] == 5
                for i in bet["values"]
                if i["value"] == "Over 2.5"
            ]
            over25_avg = round(sum(over25) / len(over25), 2)
        except ZeroDivisionError:
            over25_avg = 0
        response.append(over25_avg)
        #
        under25 = []
        try:
            under25 = [
                float(i["odd"])
                for bookmaker in self.odds["bookmakers"]
                for bet in bookmaker["bets"]
                if bet["id"] == 5
                for i in bet["values"]
                if i["value"] == "Under 2.5"
            ]
            under25_avg = round(sum(under25) / len(under25), 2)
        except ZeroDivisionError:
            under25_avg = 0
        response.append(under25_avg)

        # Both Teams Score
        btts_yes = [
            float(i["odd"])
            for bookmaker in self.odds["bookmakers"]
            for bet in bookmaker["bets"]
            if bet["id"] == 8
            for i in bet["values"]
            if i["value"] == "Yes"
        ]
        btts_yes_avg = round(sum(btts_yes) / len(btts_yes), 2)
        response.append(btts_yes_avg)
        #
        btts_no = [
            float(i["odd"])
            for bookmaker in self.odds["bookmakers"]
            for bet in bookmaker["bets"]
            if bet["id"] == 8
            for i in bet["values"]
            if i["value"] == "No"
        ]
        btts_no_avg = round(sum(btts_no) / len(btts_no), 2)
        response.append(btts_no_avg)

        logging.info(
            f"Averages: 3-Way 1H {home_fh_avg}-{draw_fh_avg}-{away_fh_avg} | "
            f"3-Way FT {home_avg}-{draw_avg}-{away_avg} | "
            f"Over/Under (2.5) {over25_avg}-{under25_avg} | "
            f"Both Teams Score {btts_yes_avg}-{btts_no_avg}"
        )

        return response


if __name__ == "__main__":
    today = date.today() - timedelta(days=1)
    week = today.isocalendar().week

    with open(f"outputs/week-{week}/fixtures/{today}.json", "r") as f:
        fixtures = json.loads(f.read())
    with open(f"outputs/week-{week}/odds/{today}.json", "r") as f:
        odds = json.loads(f.read())

    for fixture in fixtures:
        for odd in odds:
            if fixture["fixture"]["id"] == odd["fixture"]["id"]:
                analyze = Analyze(fixture, odd)
                analyze.calculate_average_odds()
                break
