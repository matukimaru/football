import logging

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s : %(message)s",
)


headers = [
    "Fixture ID",
    "Home",
    "Draw",
    "Away",
    "Home 1H",
    "Draw 1H",
    "Away 1H",
    "Over 2.5",
    "Under 2.5",
    "BTTS Yes",
    "BTTS No",
    "Status",
    "Home Sc 1H",
    "Away Sc 1H",
    "Home Sc",
    "Away Sc",
]


def calculate_status(fixture: dict, odds: dict) -> list:
    # if an odd does not exist, return 0
    data = [fixture["fixture"]["id"]]

    # Match Winner
    try:
        home = [
            float(i["odd"])
            for bookmaker in odds["bookmakers"]
            for bet in bookmaker["bets"]
            if bet["id"] == 1
            for i in bet["values"]
            if i["value"] == "Home"
        ]
        home_avg = round(sum(home) / len(home), 2)
    except ZeroDivisionError:
        home_avg = 0
    data.append(home_avg)
    #
    try:
        draw = [
            float(i["odd"])
            for bookmaker in odds["bookmakers"]
            for bet in bookmaker["bets"]
            if bet["id"] == 1
            for i in bet["values"]
            if i["value"] == "Draw"
        ]
        draw_avg = round(sum(draw) / len(draw), 2)
    except ZeroDivisionError:
        draw_avg = 0
    data.append(draw_avg)
    #
    try:
        away = [
            float(i["odd"])
            for bookmaker in odds["bookmakers"]
            for bet in bookmaker["bets"]
            if bet["id"] == 1
            for i in bet["values"]
            if i["value"] == "Away"
        ]
        away_avg = round(sum(away) / len(away), 2)
    except ZeroDivisionError:
        away_avg = 0
    data.append(away_avg)

    # First Half Winner
    try:
        home_fh = [
            float(i["odd"])
            for bookmaker in odds["bookmakers"]
            for bet in bookmaker["bets"]
            if bet["id"] == 13
            for i in bet["values"]
            if i["value"] == "Home"
        ]
        home_fh_avg = round(sum(home_fh) / len(home_fh), 2)
    except ZeroDivisionError:
        home_fh_avg = 0
    data.append(home_fh_avg)
    #
    try:
        draw_fh = [
            float(i["odd"])
            for bookmaker in odds["bookmakers"]
            for bet in bookmaker["bets"]
            if bet["id"] == 13
            for i in bet["values"]
            if i["value"] == "Draw"
        ]
        draw_fh_avg = round(sum(draw_fh) / len(draw_fh), 2)
    except ZeroDivisionError:
        draw_fh_avg = 0
    data.append(draw_fh_avg)
    #
    try:
        away_fh = [
            float(i["odd"])
            for bookmaker in odds["bookmakers"]
            for bet in bookmaker["bets"]
            if bet["id"] == 13
            for i in bet["values"]
            if i["value"] == "Away"
        ]
        away_fh_avg = round(sum(away_fh) / len(away_fh), 2)
    except ZeroDivisionError:
        away_fh_avg = 0
    data.append(away_fh_avg)

    # Over/Under 2.5
    over25 = []
    try:
        over25 = [
            float(i["odd"])
            for bookmaker in odds["bookmakers"]
            for bet in bookmaker["bets"]
            if bet["id"] == 5
            for i in bet["values"]
            if i["value"] == "Over 2.5"
        ]
        over25_avg = round(sum(over25) / len(over25), 2)
    except ZeroDivisionError:
        over25_avg = 0
    data.append(over25_avg)
    #
    under25 = []
    try:
        under25 = [
            float(i["odd"])
            for bookmaker in odds["bookmakers"]
            for bet in bookmaker["bets"]
            if bet["id"] == 5
            for i in bet["values"]
            if i["value"] == "Under 2.5"
        ]
        under25_avg = round(sum(under25) / len(under25), 2)
    except ZeroDivisionError:
        under25_avg = 0
    data.append(under25_avg)

    # Both Teams Score
    try:
        btts_yes = [
            float(i["odd"])
            for bookmaker in odds["bookmakers"]
            for bet in bookmaker["bets"]
            if bet["id"] == 8
            for i in bet["values"]
            if i["value"] == "Yes"
        ]
        btts_yes_avg = round(sum(btts_yes) / len(btts_yes), 2)
    except ZeroDivisionError:
        btts_yes_avg = 0
    data.append(btts_yes_avg)
    #
    try:
        btts_no = [
            float(i["odd"])
            for bookmaker in odds["bookmakers"]
            for bet in bookmaker["bets"]
            if bet["id"] == 8
            for i in bet["values"]
            if i["value"] == "No"
        ]
        btts_no_avg = round(sum(btts_no) / len(btts_no), 2)
    except ZeroDivisionError:
        btts_no_avg = 0
    data.append(btts_no_avg)

    # Outcomes
    data.append(fixture["fixture"]["status"]["short"])
    data.append(fixture["score"]["halftime"]["home"])
    data.append(fixture["score"]["halftime"]["away"])
    data.append(fixture["score"]["fulltime"]["home"])
    data.append(fixture["score"]["fulltime"]["away"])

    # logging.info(
    #     f"Averages: 3-Way FT {home_fh_avg}-{draw_fh_avg}-{away_fh_avg} | "
    #     f"3-Way 1H {home_avg}-{draw_avg}-{away_avg} | "
    #     f"Over/Under (2.5) {over25_avg}-{under25_avg} | "
    #     f"Both Teams Score {btts_yes_avg}-{btts_no_avg}"
    # )

    return data
