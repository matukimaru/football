headers = [
    "FxId",  # 0    fixture id
    "FxDt",  # 1    fixture date
    "FxName",  # 2  fixture name
    "OdHm",  # 3    odd home win
    "OdDr",  # 4    odd draw
    "OdAw",  # 5    odd away win
    "OdHmH",  # 6  odd home win first half
    "OdDrH",  # 7  odd draw first half
    "OdAwH",  # 8  odd away win first half
    "OdOv2",  # 9  odd over 2.5
    "OdUn2",  # 10  odd under 2.5
    "OdBtY",  # 11  odd both teams to score
    "OdBtN",  # 12 odd both teams not to score
    "Sts",  # 13    fixture status
    "RsHmH",  # 14 result home first half
    "RsAwH",  # 15 result away first half
    "RsHmF",  # 16 result home full time
    "RsAwF",  # 17 result away full time
    "PrWnr",  # 18  prediction winner
    "PrGlHm",  # 19 prediction goals home
    "PrGlAw",  # 20 prediction goals away
    "PrPrHm",  # 21 prediction percent home
    "PrPrDr",  # 22 prediction percent draw
    "PrPrAw",  # 23 prediction percent away
    "PrFmHm",  # 24 prediction form home
    "PrFmAw",  # 25 prediction form away
    "PrAtHm",  # 26 prediction attack home
    "PrAtAw",  # 27 prediction attack away
    "PrDfHm",  # 28 prediction defence home
    "PrDfAw",  # 29 prediction defence away
    "L5GfHm",  # 30 last 5 goals for home
    "L5GaHm",  # 31 last 5 goals against home
    "L5GfAw",  # 32 last 5 goals for away
    "L5GaAw",  # 33 last 5 goals against away
    "LgFmHm",  # 34 league form home
    "LgFmAw",  # 35 league form away
]


def extract_data(fixture: dict, odds: dict, prediction: dict) -> list:
    # id, date, name (0-2)
    data = [
        fixture["fixture"]["id"],
        fixture["fixture"]["date"],
        f'{fixture["teams"]["home"]["name"]} v {fixture["teams"]["away"]["name"]}',
    ]

    # Match Winner (3-5)
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

    # First Half Winner (6-8)
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

    # Over/Under 2.5 (9-10)
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

    # Both Teams Score (11-12)
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

    # Outcomes (13-17)
    data.append(fixture["fixture"]["status"]["short"])
    data.append(fixture["score"]["halftime"]["home"])
    data.append(fixture["score"]["halftime"]["away"])
    data.append(fixture["score"]["fulltime"]["home"])
    data.append(fixture["score"]["fulltime"]["away"])

    # prediction winner (18)
    try:
        data.append(prediction["predictions"]["winner"]["name"])
    except KeyError:
        data.append("-")
    # prediction goals (19-20)
    try:
        data.append(prediction["predictions"]["goals"]["home"])
    except KeyError:
        data.append("-")
    try:
        data.append(prediction["predictions"]["goals"]["away"])
    except KeyError:
        data.append("-")
    # prediction percentages (21-23)
    try:
        data.append(prediction["predictions"]["percent"]["home"])
    except KeyError:
        data.append("-")
    try:
        data.append(prediction["predictions"]["percent"]["draw"])
    except KeyError:
        data.append("-")
    try:
        data.append(prediction["predictions"]["percent"]["away"])
    except KeyError:
        data.append("-")
    # prediction form (24-25)
    try:
        data.append(prediction["teams"]["home"]["last_5"]["form"])
    except KeyError:
        data.append("-")
    try:
        data.append(prediction["teams"]["away"]["last_5"]["form"])
    except KeyError:
        data.append("-")
    # prediction attack (26-27)
    try:
        data.append(prediction["teams"]["home"]["last_5"]["att"])
    except KeyError:
        data.append("-")
    try:
        data.append(prediction["teams"]["away"]["last_5"]["att"])
    except KeyError:
        data.append("-")
    # prediction defence (28-29)
    try:
        data.append(prediction["teams"]["home"]["last_5"]["def"])
    except KeyError:
        data.append("-")
    try:
        data.append(prediction["teams"]["away"]["last_5"]["def"])
    except KeyError:
        data.append("-")
    # last 5 goals home (30-31)
    try:
        data.append(prediction["teams"]["home"]["last_5"]["goals"]["for"]["total"])
    except KeyError:
        data.append("-")
    try:
        data.append(prediction["teams"]["home"]["last_5"]["goals"]["against"]["total"])
    except KeyError:
        data.append("-")
    # last 5 goals away (32-33)
    try:
        data.append(prediction["teams"]["away"]["last_5"]["goals"]["for"]["total"])
    except KeyError:
        data.append("-")
    try:
        data.append(prediction["teams"]["away"]["last_5"]["goals"]["against"]["total"])
    except KeyError:
        data.append("-")
    # league form (34-35)
    try:
        data.append(prediction["teams"]["home"]["league"]["form"])
    except KeyError:
        data.append("-")
    try:
        data.append(prediction["teams"]["away"]["league"]["form"])
    except KeyError:
        data.append("-")

    return data
