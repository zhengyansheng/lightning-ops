import datetime

import pytz
from xpinyin import Pinyin

def convert_from_utc(date_time, time_zone):
    tz = pytz.timezone(time_zone)
    utc = pytz.timezone('UTC')
    return date_time.replace(tzinfo=utc).astimezone(tz)


def utc2local(utc_dtm):
    # UTC时间转本地时间
    local_tm = datetime.datetime.fromtimestamp(0)
    utc_tm = datetime.datetime.utcfromtimestamp(0)
    offset = local_tm - utc_tm
    return utc_dtm + offset


def local2utc(local_dtm):
    # 本地时间转UTC时间
    return datetime.datetime.utcfromtimestamp(local_dtm.timestamp())


def time_utcstr_localstr(utcstr, format='%Y-%m-%d %H:%M:%S'):
    UTC_FORMAT = "%Y-%m-%dT%H:%M:%S.%fZ"
    utcTime = datetime.datetime.strptime(utcstr, UTC_FORMAT)
    localtime = utcTime + datetime.timedelta(hours=8)
    return localtime.strftime(format)


def time_utcstr_localtime(utcstr, format='%Y-%m-%d %H:%M:%S'):
    UTC_FORMAT = "%Y-%m-%dT%H:%M:%S.%fZ"
    utcTime = datetime.datetime.strptime(utcstr, UTC_FORMAT)
    localtime = utcTime + datetime.timedelta(hours=8)
    return localtime


def chinese_to_pinyin(s):
    p = Pinyin()
    return p.get_pinyin(s).replace("-", "")