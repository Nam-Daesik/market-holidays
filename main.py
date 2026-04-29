import csv
import os
import holidays
from datetime import date, timedelta
from itertools import zip_longest

def get_early_closes(year):
    early_closes = []
    if date(year, 7, 4).weekday() != 5:
        d = date(year, 7, 3)
        if d.weekday() < 5: early_closes.append(d)
    nov_first = date(year, 11, 1)
    wday = nov_first.weekday()
    days_to_thursday = (3 - wday + 7) % 7
    thanksgiving = nov_first + timedelta(days=days_to_thursday) + timedelta(weeks=3)
    early_closes.append(thanksgiving + timedelta(days=1))
    xmas_eve = date(year, 12, 24)
    if xmas_eve.weekday() < 5: early_closes.append(xmas_eve)
    return early_closes

today = date.today()
today_str = today.strftime("%Y-%m-%d")
end_date = today + timedelta(days=730) 

past_holidays = []
past_early = []

if os.path.exists("holidays.csv"):
    with open("holidays.csv", "r", encoding="utf-8") as f:
        reader = csv.reader(f)
        next(reader, None)
        for row in reader:
            if len(row) > 0 and row[0] and row[0] < today_str:
                past_holidays.append(row[0])
            if len(row) > 1 and row[1] and row[1] < today_str:
                past_early.append(row[1])

new_holidays = []
new_early = []
target_years = range(today.year, end_date.year + 1)
nyse_holidays = holidays.NYSE(years=target_years)

for d in sorted(nyse_holidays.keys()):
    if today <= d <= end_date:
        new_holidays.append(d.strftime("%Y-%m-%d"))

for y in target_years:
    for ed in get_early_closes(y):
        if today <= ed <= end_date:
            new_early.append(ed.strftime("%Y-%m-%d"))

final_holidays = sorted(list(set(past_holidays + new_holidays)))
final_early = sorted(list(set(past_early + new_early)))

with open("holidays.csv", "w", newline="", encoding="utf-8") as f:
    writer = csv.writer(f)
    writer.writerow(["Holidays", "Early_Closes"])
    for h, e in zip_longest(final_holidays, final_early, fillvalue=""):
        writer.writerow([h, e])
