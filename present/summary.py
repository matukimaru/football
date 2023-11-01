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
    # "2023-10-17",
    # "2023-10-18",
]
weeks = [datetime.strptime(date, date_format).isocalendar().week for date in dates]
