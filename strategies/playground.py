# condition 1
# if (
#     1.95 <= match_winner[0] <= 2.15
#     or 1.95 <= match_winner[1] <= 2.15
#     or 1.95 <= match_winner[2] <= 2.15
# ):
#     count += 1
#     print(f"{match_winner[0]} : {match_winner[1]} : {match_winner[2]}")

# # condition 2
# if (match_winner[0] >= 2.2 and match_winner[2] >= 2.2) and (
#     abs(match_winner[0] - match_winner[2]) <= 0.2
# ):
#     count += 1
#     print(f"{match_winner[0]} : {match_winner[1]} : {match_winner[2]}")


from datetime import date, timedelta

from summary import daily
from tabulate import tabulate

data = daily(date.today() - timedelta(days=1), 41)

# over = [
#     data[0],
# ]

# for i in range(len(data)):
#     if i == 0:
#         pass
#     else:
#         #
#         if (data[i][7] + data[i][8]) >= 3 and data[i][4] < data[i][5]:
#             over.append(data[i])

# print(tabulate(over, headers="firstrow", showindex="always", tablefmt="simple"))


# 3-way full time (home biased)
match_winner = [
    data[0],
]
count = [0, 0, 0, 0, 0]  # total,over-biased,over-won,under-biased,under-won
# filter by range of odds
for i in range(len(data)):
    if i == 0:
        pass
    else:
        # odd range
        if 1.75 <= data[i][1] <= 2.05:
            count[0] += 1
            # over biased
            if data[i][4] > data[i][5]:
                count[1] += 1
                try:
                    if data[i][7] >= data[i][8]:
                        count[2] += 1
                except IndexError:
                    pass

            # under biased
            if data[i][4] < data[i][5]:
                count[3] += 1
                try:
                    if data[i][7] >= data[i][8]:
                        count[4] += 1
                except IndexError:
                    pass

            # match_winner.append(data[i])

print(count)
print(
    f"Total: {count[0]}, Over-biased: {count[1]}, Over-won: {count[2]}, Under-biased: {count[3]}, Under-won: {count[4]}"
)
# print(tabulate(match_winner, headers="firstrow", showindex="always", tablefmt="simple"))
