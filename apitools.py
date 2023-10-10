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
