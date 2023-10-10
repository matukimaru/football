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
