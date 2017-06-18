from datetime import datetime
from math import log
import pytz

epoch = datetime(1970, 1, 1, 0, 0, 0, 0)
epoch_localized = epoch.replace(tzinfo=pytz.utc)


def epoch_seconds(created_time):
    td = created_time - epoch_localized
    return td.days * 86400 + td.seconds + (float(td.microseconds) / 1000000)


def score(ups, downs):
    return ups - downs


def _popularity(ups, downs, created_time):
    s = score(ups, downs)
    order = log(max(abs(s), 1), 10)
    sign = 1 if s > 0 else -1 if s < 0 else 0
    seconds = epoch_seconds(created_time) - 1134028003
    return round(sign * order + seconds / 45000, 7)
