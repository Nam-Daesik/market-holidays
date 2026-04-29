import pandas_market_calendars as mcal
import pandas as pd
from datetime import date, timedelta
import csv
from itertools import zip_longest
import pytz

today = date.today()
end_date = today + timedelta(days=730)
start_date_str = '2010-01-01'
end_date_str = end_date.strftime('%Y-%m-%d')

nyse = mcal.get_calendar('NYSE')
schedule = nyse.schedule(start_date=start_date_str, end_date=end_date_str)

all_weekdays = pd.bdate_range(start=start_date_str, end=end_date_str)
trading_days = schedule.index.tz_localize(None)
mcal_holidays = all_weekdays.difference(trading_days)
holidays_list = sorted([d.strftime('%Y-%m-%d') for d in mcal_holidays])

early_closes_list = []
est_tz = pytz.timezone('America/New_York')

for index, row in schedule.iterrows():
    if row['market_close'].astimezone(est_tz).hour < 16:
        early_closes_list.append(index.strftime('%Y-%m-%d'))

early_closes_list = sorted(early_closes_list)

with open("holidays.csv", "w", newline="", encoding="utf-8") as f:
    writer = csv.writer(f)
    writer.writerow(["Holidays", "Early_Closes"])
    for h, e in zip_longest(holidays_list, early_closes_list, fillvalue=""):
        writer.writerow([h, e])
