headers = [
    "FxId",  # 0    fixture id
    "OdHm",  # 1    odd home win
    "OdDr",  # 2    odd draw
    "OdAw",  # 3    odd away win
    "OdHmH",  # 4  odd home win first half
    "OdDrH",  # 5  odd draw first half
    "OdAwH",  # 6  odd away win first half
    "OdOv2",  # 7  odd over 2.5
    "OdUn2",  # 8  odd under 2.5
    "OdBtY",  # 9  odd both teams to score
    "OdBtN",  # 10 odd both teams not to score
    "Sts",  # 11    fixture status
    "RsHmH",  # 12 result home first half
    "RsAwH",  # 13 result away first half
    "RsHmF",  # 14 result home full time
    "RsAwF",  # 15 result away full time
]

new_headers = [
    "FxId",  # 0    fixture id
    "OdHm",  # 1    odd home win
    "OdDr",  # 2    odd draw
    "OdAw",  # 3    odd away win
    "OdHmH",  # 4  odd home win first half
    "OdDrH",  # 5  odd draw first half
    "OdAwH",  # 6  odd away win first half
    "OdOv2",  # 7  odd over 2.5
    "OdUn2",  # 8  odd under 2.5
    "OdBtY",  # 9  odd both teams to score
    "OdBtN",  # 10 odd both teams not to score
    "Sts",  # 11    fixture status
    "RsHmH",  # 12 result home first half
    "RsAwH",  # 13 result away first half
    "RsHmF",  # 14 result home full time
    "RsAwF",  # 15 result away full time
    "PrWnr",  # 16  prediction winner
    "PrGlHm",  # 17 prediction goals home
    "PrGlAw",  # 18 prediction goals away
    "PrPrHm",  # 19 prediction percent home
    "PrPrDr",  # 20 prediction percent draw
    "PrPrAw",  # 21 prediction percent away
    "PrFmHm",  # 22 prediction form home
    "PrFmAw",  # 23 prediction form away
    "PrAtHm",  # 24 prediction attack home
    "PrAtAw",  # 25 prediction attack away
    "PrDfHm",  # 26 prediction defence home
    "PrDfAw",  # 27 prediction defence away
    "L5GfHm",  # 28 last 5 goals for home
    "L5GaHm",  # 29 last 5 goals against home
    "LfGfAw",  # 30 last 5 goals for away
    "L5GaAw",  # 31 last 5 goals against away
    "LgFmHm",  # 32 league form home
    "LgFmAw",  # 33 league form away
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
