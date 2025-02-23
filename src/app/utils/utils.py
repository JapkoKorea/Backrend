import pytz
from datetime import datetime


def get_korea_time():
    korea_tz = pytz.timezone("Asia/Seoul")
    utc_now = datetime.now(pytz.utc)
    korea_time = utc_now.astimezone(korea_tz)
    return korea_time.strftime("%Y-%m-%dT%H:%M:%S")  # ISO 8601