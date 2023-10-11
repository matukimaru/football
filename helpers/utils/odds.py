def calculate_averages(odd: list) -> list:
    response = [odd["fixture"]["id"]]

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

    over25 = [
        float(i["odd"])
        for bookmaker in odd["bookmakers"]
        for bet in bookmaker["bets"]
        if bet["id"] == 5
        for i in bet["values"]
        if i["value"] == "Over 2.5"
    ]
    try:
        over25_avg = round(sum(over25) / len(over25), 2)
    except ZeroDivisionError:
        over25_avg = 0
    response.append(over25_avg)

    under25 = [
        float(i["odd"])
        for bookmaker in odd["bookmakers"]
        for bet in bookmaker["bets"]
        if bet["id"] == 5
        for i in bet["values"]
        if i["value"] == "Under 2.5"
    ]
    try:
        under25_avg = round(sum(under25) / len(under25), 2)
    except ZeroDivisionError:
        under25_avg = 0
    response.append(under25_avg)

    return response


def calculate_outcomes(fixture: dict) -> list:
    response = [fixture["id"]]

    return response
