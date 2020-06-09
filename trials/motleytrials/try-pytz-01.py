import pytz
import tzlocal
import datetime
import time
import calendar
fmt1 = '%Y-%m-%d %H:%M:%S.%f %Z%z'
t1   = (2019,5,14,18,30,10,123456)
dt1  = datetime.datetime(t1[0],t1[1],t1[2],t1[3],t1[4],t1[5],t1[6])   # naive dt, but in utc
print(f't1={t1}')
print("dt1=" + dt1.strftime(fmt1) + " (naive utc)")
print("dt1.utctimetuple()=",end="")
print(dt1.utctimetuple())
ts1 = calendar.timegm(dt1.utctimetuple())
ts2 = ts1 + (dt1.microsecond/1000000.0)
print(f'ts1={ts1}')
print(f'ts2={ts2}')
tz_loc = tzlocal.get_localzone()
tz_la  = pytz.timezone("America/Los_Angeles")
tz_utc = pytz.utc
print("tz_loc=" + str(tz_loc))
print("tz_la =" + str(tz_la))
print("tz_utc=" + str(tz_utc))
dt2 = pytz.utc.localize(dt1)
print("dt2=" + dt2.strftime(fmt1) + " (localized utc)")
dt3 = dt2.astimezone(tz_la)
print("dt3=" + dt3.strftime(fmt1) + " (localized la)")
dt4 = dt2.astimezone(tz_loc)
print("dt4=" + dt4.strftime(fmt1) + " (localized loc)")
dt5 = dt2.astimezone(tz_utc)
print("dt5=" + dt5.strftime(fmt1) + " (localized utc)")
if True:
    count = 0
    for tzname in pytz.all_timezones:
        count = count + 1
        print(f'{count}: {tzname}')
print("done")
