import math


def correct_score_first_half(data: list) -> list:
    results = []
    for fixture in data:
        # odds (over/under) exist
        if fixture[9] and fixture[10]:
            # under 2.5 odds are favoured
            if fixture[9] > fixture[10]:
                # goals prediction exists
                if fixture[19] and fixture[20]:
                    # where goals prediction = 3.0
                    if abs(float(fixture[19])) + abs(float(fixture[20])) == 3.0:
                        results.append(fixture)
    return results


# can also be used for away team to win (draw no bet)
def both_teams_to_score(data: list) -> list:
    results = []
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
                        if abs(float(fixture[19])) + abs(float(fixture[20])) >= 5.0:
                            results.append(fixture)
    return results


def test(data: list) -> list:
    result = []
    tallies = [0, 0, 0, 0, 0, 0, 0, 0]

    for fixture in data:
        # completed fixtures only
        if fixture[13] == "FT" or fixture[13] == "PEN":
            # if 1.8 <= fixture[5] <= 2.3:
            if fixture[3] > fixture[5]:
                if fixture[18] == 2:
                    if fixture[19] and fixture[20]:
                        tallies[0] += 1
                        result.append(fixture)
                        if abs(float(fixture[19])) + abs(float(fixture[20])) >= 5.0:
                            tallies[1] += 1
                            # result.append(fixture)

            # if fixture[19] and fixture[20]:
            #     if abs(float(fixture[19])) + abs(float(fixture[20])) >= 5.0:
            #         tallies[1] += 1

    print(f"total: {tallies[0]}")
    print(f"  away favoured: {tallies[1]}")

    # hts = tallies[2] + tallies[3] + tallies[4] + tallies[5]
    # print("+ hits")
    # print(f"   below 3.0: {tallies[2]} - {math.floor(tallies[2]/hts*100)}%")
    # print(f"   below 4.0: {tallies[3]} - {math.floor(tallies[3]/hts*100)}%")
    # print(f"   below 5.0: {tallies[4]} - {math.floor(tallies[4]/hts*100)}%")
    # print(f"   above 5.0: {tallies[5]} - {math.floor(tallies[5]/hts*100)}%")
    # print(
    #     f"   under better: {tallies[6]} - {math.floor(tallies[6]/(tallies[6] + tallies[7])*100)}%"
    # )

    return result
