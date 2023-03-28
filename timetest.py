from datetime import datetime
import pytz


def get_time_of_query():
    tz = pytz.timezone('Europe/London')
    now = datetime.now(tz).strftime('%y-%m-%d %H:%M:%S')
    return now

print(get_time_of_query())