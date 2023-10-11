import json

import requests
from decouple import config


class ApiSports:
    def __init__(self):
        """_summary_"""
        self.url = "https://v3.football.api-sports.io"
        # pull from environment variables
        self.application_key = config("API_KEY")
        # supplied by calling statement
        self.endpoint = ""
        self.params = {}

    @property
    def headers(self):
        """_summary_

        Returns:
            _type_: _description_
        """
        return {
            "x-rapidapi-host": "v3.football.api-sports.io",
            "x-rapidapi-key": self.application_key,
        }

    @property
    def response(self):
        """_summary_

        Returns:
            _type_: _description_
        """
        return requests.get(
            f"{self.url}{self.endpoint}", headers=self.headers, params=self.params
        ).text

    def query(self, endpoint, params={}):
        """queries a provided endpoint

        Args:
            endpoint (_type_): _description_
            params (dict, optional): _description_. Defaults to {}.

        Returns:
            _type_: _description_
        """
        self.endpoint = endpoint
        self.params = params
        return json.loads(self.response)
