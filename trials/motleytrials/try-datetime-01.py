import pytz
import tzlocal
import motleylog.motleydatetime as mdt
fmt1 = '%Y-%m-%d %H:%M:%S.%f %Z%z'
tz_utc = pytz.utc
tz_loc = tzlocal.get_localzone()
tz_list = ["UTC", "America/Los_Angeles", "America/New_York",
           "US/Pacific", "US/Mountain", "US/Central", "US/Eastern", "US/Hawaii", "US/Alaska"]
tz_dict = {}
for tzname in tz_list:
    tz_dict[tzname] = pytz.timezone(tzname)
    #print(str(pytz.timezone(tzname).__class__))

dt1 = mdt.get_utc_datetime(2019,5,14,18,30,10,123456)
print(dt1.strftime(fmt1))


def dump_dt(dt_utc):
    for tzname in tz_list:
        tz = tz_dict[tzname]
        temp_dt = dt_utc.astimezone(tz)
        print(temp_dt.strftime(fmt1),f'({tzname})')
        print(repr(temp_dt))
        print(temp_dt.tzinfo)
        print(mdt.get_epoch_from_aware_datetime(temp_dt))

dump_dt(dt1)
#dt1_epoch = mdt.get_epoch_from_aware_datetime(dt1)
#print(f'dt1_epoch={dt1_epoch}')
