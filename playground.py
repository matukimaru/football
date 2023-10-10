from datetime import date

week = date.today().isocalendar().week

print(type(week))
