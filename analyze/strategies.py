def match_winner_1(data: list) -> list:
    result = []
    for dt in data:
        # where home or away odds are within limits
        if 1.95 <= dt[3] <= 2.1 or 1.95 <= dt[5] <= 2.1:
            result.append(dt)

    return result


def match_winner_2(data: list) -> list:
    result = []
    for dt in data:
        # where difference between home and away odds is within limits
        if 0.01 <= (dt[3] - dt[5]) <= 0.2 or 0.01 <= (dt[5] - dt[3]) <= 0.2:
            result.append(dt)

    return result
