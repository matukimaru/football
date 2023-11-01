import math


def over_25(data: list) -> list:
    pass


def under_25(data: list) -> list:
    pass


def match_winner_home(data: list) -> list:
    results = []
    counts = {
        "evaluated": 0,
        "wins": 0,
        "losses": 0,
        "draws": 0,
    }
    for fixture in data:
        # match winner odds exist
        if fixture[3] and fixture[5]:
            # home is predicted to win
            if fixture[18] == 1:
                # home odds are within a range
                if 1.9 <= fixture[3] <= 2.5:
                    results.append(fixture[:-2])

                    # calculate for completed fixtures
                    try:
                        if fixture[13] == "FT" or fixture[13] == "PEN":
                            counts["evaluated"] += 1
                            if fixture[16] > fixture[17]:
                                counts["wins"] += 1
                            elif fixture[16] < fixture[17]:
                                counts["losses"] += 1
                            else:
                                counts["draws"] += 1
                    except TypeError:
                        pass

    return [results, counts]


def match_winner_away(data: list) -> list:
    results = []
    counts = {
        "evaluated": 0,
        "wins": 0,
        "losses": 0,
        "draws": 0,
        "direct": {"yes": 0, "no": 0, "draws": 0},
    }
    for fixture in data:
        # match winner odds exist
        if fixture[3] and fixture[5]:
            # away is predicted to win
            if fixture[18] == 2:
                # odds are within a range
                if 1.91 <= fixture[5] <= 2.09:
                    # if (
                    #     (int(fixture[25][:-1]) > int(fixture[24][:-1]))
                    #     and (int(fixture[27][:-1]) > int(fixture[26][:-1]))
                    #     and (int(fixture[29][:-1]) > int(fixture[28][:-1]))
                    # ):
                    results.append(fixture[:-2])

                    # calculate for completed fixtures
                    try:
                        if fixture[13] == "FT" or fixture[13] == "PEN":
                            counts["evaluated"] += 1
                            if fixture[16] < fixture[17]:
                                counts["wins"] += 1
                            elif fixture[16] > fixture[17]:
                                counts["losses"] += 1
                            else:
                                counts["draws"] += 1

                            # check GGs
                            # if fixture[16] > 0 and fixture[17] > 0:
                            #     counts["ggs"] += 1

                            # interestingly all won
                            if int(fixture[23][:-1]) == 50:
                                # results.append(fixture[:-2])
                                if fixture[17] > fixture[16]:
                                    counts["direct"]["yes"] += 1
                                elif fixture[17] < fixture[16]:
                                    counts["direct"]["no"] += 1
                                else:
                                    counts["direct"]["draws"] += 1
                    except TypeError:
                        pass

    return [results, counts]


def both_teams_to_score_yes(data: list) -> list:
    results = []
    counts = {
        "evaluated": 0,
        "wins": 0,
        "losses": 0,
    }
    for fixture in data:
        # if match winner odds exist
        if fixture[3] and fixture[5]:
            # odds favour away team
            if fixture[3] > fixture[5]:
                # away team is predicted to win
                if fixture[18] == 2:
                    # goals prediction exists
                    if fixture[19] and fixture[20]:
                        # total goals is >= 5.0
                        if abs(float(fixture[19])) + abs(float(fixture[20])) >= 0.0:
                            if sum(fixture[30:34]) >= 40:
                                try:
                                    counts["evaluated"] += 1
                                    if fixture[16] > 0 and fixture[17] > 0:
                                        counts["wins"] += 1
                                    else:
                                        counts["losses"] += 1
                                except TypeError:
                                    pass

                            results.append(fixture[:-2])
    return [results, counts]


def both_teams_to_score_no(data: list) -> list:
    pass


def gg_yes(data: list) -> list:
    pass


def gg_no(data: list) -> list:
    pass
