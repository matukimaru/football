import json

import requests
from decouple import config


class API:
    def __init__(self):
        self.url = "https://v3.football.api-sports.io"
        self.application_key = config("API_KEY")
        self.endpoint = ""
        self.params = {}

    @property
    def headers(self):
        return {
            "x-rapidapi-host": "v3.football.api-sports.io",
            "x-rapidapi-key": self.application_key,
        }

    @property
    def response(self):
        return requests.get(
            f"{self.url}{self.endpoint}", headers=self.headers, params=self.params
        ).text

    def query(self, endpoint, params={}):
        self.endpoint = endpoint
        self.params = params
        return json.loads(self.response)


def calculate_match_winner_odds(odd: list) -> list:
    response = []

    home = [
        float(i["odd"])
        for bookmaker in odd["bookmakers"]
        for bet in bookmaker["bets"]
        if bet["id"] == 1
        for i in bet["values"]
        if i["value"] == "Home"
    ]
    home_avg = round(sum(home) / len(home), 2)
    response.append(home_avg)

    draw = [
        float(i["odd"])
        for bookmaker in odd["bookmakers"]
        for bet in bookmaker["bets"]
        if bet["id"] == 1
        for i in bet["values"]
        if i["value"] == "Draw"
    ]
    draw_avg = round(sum(draw) / len(draw), 2)
    response.append(draw_avg)

    away = [
        float(i["odd"])
        for bookmaker in odd["bookmakers"]
        for bet in bookmaker["bets"]
        if bet["id"] == 1
        for i in bet["values"]
        if i["value"] == "Away"
    ]
    away_avg = round(sum(away) / len(away), 2)
    response.append(away_avg)

    return response
