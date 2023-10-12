import json
import logging
from time import sleep

from apiutils import ApiSports

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s : %(message)s",
)

api = ApiSports()

with open("outputs/week-41/fixtures/2023-10-12.json", "r") as f:
    fixtures = json.loads(f.read())

predictions = []

count = 0
for fixture in fixtures:
    params = {"fixture": fixture["fixture"]["id"]}
    response = api.query("/predictions", params)
    count += 1
    if not len(response["errors"]):
        predictions.append(response["response"][0])
        logging.info(
            f"{fixture['teams']['home']['name']} vs {fixture['teams']['away']['name']}"
        )
        if count % 10 == 0:
            logging.info(f"sleeping for a minute")
            sleep(61)
    else:
        logging.error(f"{response['errors']}")

with open("resources/predictions.json", "w+") as f:
    f.write(json.dumps(predictions))
