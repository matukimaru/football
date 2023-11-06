import math

from analyzer import HEADERS, Analyze
from tabulate import tabulate
from utils import headers

dates = [
    "2023-11-05",
]

analyzer = Analyze(dates)

# Avoid fixtures without a prediction or that are missing any odds
data = [
    d
    for d in analyzer.data
    if 0 not in d[4:13] and "--" not in d
    if 2.1 <= d[4] <= 3.2 and 2.1 <= d[4] <= 3.2
]
print(tabulate(data, headers=HEADERS, showindex="always", tablefmt="simple"))

# won = [d for d in data if d[18] == "Won"]
# lost = [d for d in data if d[18] == "Lost"]
# others = [d for d in data if (d[18]) == "PST" or (d[18] == "ABD")]
# res = f"""
# --
# Won:    {len(won)}\t- {math.floor(len(won)*100/(len(won) + len(lost)))}%
# Lost:   {len(lost)}\t- {math.floor(len(lost)*100/(len(won) + len(lost)))}%
# Others: {len(others)}
# --
# Total:  {len(data)}
# """
# print(res)

# print(analyzer.betslips, len(analyzer.betslips))
