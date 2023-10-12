import logging

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s : %(message)s",
)


headers = [
    "Fixture ID",  # 0
    "Home",  # 1
    "Draw",  # 2
    "Away",  # 3
    "Home 1H",  # 4
    "Draw 1H",  # 5
    "Away 1H",  # 6
    "Over 2.5",  # 7
    "Under 2.5",  # 8
    "BTTS Yes",  # 9
    "BTTS No",  # 10
    "Status",  # 11
    "Home Sc 1H",  # 12
    "Away Sc 1H",  # 13
    "Home Sc",  # 14
    "Away Sc",  # 15
]

new_headers = [  # 18
    "Fixture ID",  # 0
    "Home",  # 1
    "Draw",  # 2
    "Away",  # 3
    "Home 1H",  # 4
    "Draw 1H",  # 5
    "Away 1H",  # 6
    "Over 2.5",  # 7
    "Under 2.5",  # 8
    "BTTS Yes",  # 9
    "BTTS No",  # 10
    "Status",  # 11
    "Home Sc 1H",  # 12
    "Away Sc 1H",  # 13
    "Home Sc",  # 14
    "Away Sc",  # 15
    "Winner",  # 16
    "G-Home",  # 17
    "G-Away",  # 18
    "P-Hm",  # 19
    "P-Dr",  # 20
    "P-Aw",  # 21
    "F-Hm",  # 22
    "F-Aw",  # 23
    "At-Hm",  # 24
    "At-Aw",  # 25
    "Df-Hm",  # 26
    "Df-Aw",  # 27
    "GF-Hm",  # 28
    "GA-Hm",  # 29
    "GF-Aw",  # 30
    "GA-Aw",  # 31
    "LG-Hm",  # 32
    "LG-Aw",  # 33
]


def calculate_status(fixture: dict, odds: dict) -> list:
    # if an odd does not exist, set it to0
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
    except Exception:
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
    except Exception:
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
    except Exception:
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
    except Exception:
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
    except Exception:
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
    except Exception:
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
    except Exception:
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
    except Exception:
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
    except Exception:
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
    except Exception:
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
