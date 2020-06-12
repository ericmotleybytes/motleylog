import unittest
import datetime
import pytz
import tzlocal
import sys
import motleylog.motleydatetime as mdt
class TestMotleyDatetime(unittest.TestCase):

    fmt = '%Y-%m-%d %H:%M:%S.%f %Z%z'

    def test_get_utc_datetime(self):
        dt_utc = mdt.get_utc_datetime(2019, 5, 14, 18, 30, 10, 123456)
        expect = "2019-05-14 18:30:10.123456 UTC+0000"
        actual = dt_utc.strftime(self.fmt)
        self.assertEqual(expect,actual)
        dt_utc = mdt.get_utc_datetime(2019, 5, 14)
        expect = "2019-05-14 00:00:00.000000 UTC+0000"
        actual = dt_utc.strftime(self.fmt)
        self.assertEqual(expect,actual)

    def test_is_naive(self):
        naive_dt = datetime.datetime(2019, 5, 14, 18, 30, 10, 123456)
        self.assertEqual(True,mdt.is_naive(naive_dt))
        aware_dt = mdt.get_utc_datetime(2019, 5, 14, 18, 30, 10, 123456)
        self.assertEqual(False,mdt.is_naive(aware_dt))
        try:
            result = mdt.is_naive("dummy")
            self.fail("Expected TypeError exception not raised.")
        except TypeError:
            self.assertTrue(True,"Expected this exception.")
        except:
            self.fail("Unexpected exception: " + sys.exc_info()[0])

    def test_is_aware(self):
        naive_dt = datetime.datetime(2019, 5, 14, 18, 30, 10, 123456)
        self.assertEqual(False,mdt.is_aware(naive_dt))
        aware_dt = mdt.get_utc_datetime(2019, 5, 14, 18, 30, 10, 123456)
        self.assertEqual(True,mdt.is_aware(aware_dt))

    def test_get_aware_datetime(self):
        local_tz_str = str(tzlocal.get_localzone())
        default_dt = mdt.get_aware_datetime(2019, 5, 14, 18, 30, 10, 123456)
        self.assertEqual(True,mdt.is_aware(default_dt))
        default_tz_str = str(default_dt.tzinfo)
        self.assertEqual(local_tz_str,default_tz_str)
        utc_dt = mdt.get_aware_datetime(2019, 5, 14, 18, 30, 10, 123456, pytz.utc)
        expect = "2019-05-14 18:30:10.123456 UTC+0000"
        actual = utc_dt.strftime(self.fmt)
        self.assertEqual(expect,actual)
        utc_dt = mdt.get_aware_datetime(2019, 5, 14, 18, 30, 10, 123456, "UTC")
        expect = "2019-05-14 18:30:10.123456 UTC+0000"
        actual = utc_dt.strftime(self.fmt)
        self.assertEqual(expect,actual)

    def test_get_epoch_from_aware_datetime(self):
        aware_dt = mdt.get_aware_datetime(2019, 5, 14, 18, 30, 10, 123456,"UTC")
        epoch = mdt.get_epoch_from_aware_datetime(aware_dt)
        #expect = 1557858610.123456
        self.assertTrue(epoch>0.0)
        aware_dt2 = mdt.get_aware_datetime_from_epoch(epoch,"UTC")
        expect = "2019-05-14 18:30:10.123456 UTC+0000"
        actual = aware_dt2.strftime(self.fmt)
        self.assertEqual(expect,actual)

    def test_get_utc_datetime_from_epoch(self):
        aware_dt = mdt.get_aware_datetime(2019, 5, 14, 18, 30, 10, 123456, "UTC")
        epoch = mdt.get_epoch_from_aware_datetime(aware_dt)
        utc_dt = mdt.get_utc_datetime_from_epoch(epoch)
        expect = "2019-05-14 18:30:10.123456 UTC+0000"
        actual = utc_dt.strftime(self.fmt)
        self.assertEqual(expect,actual)

    def test_get_aware_datetime_from_epoch(self):
        aware_dt = mdt.get_aware_datetime(2019, 5, 14, 18, 30, 10, 123456, "UTC")
        epoch = mdt.get_epoch_from_aware_datetime(aware_dt)
        utc_dt = mdt.get_aware_datetime_from_epoch(epoch,"UTC")
        expect = "2019-05-14 18:30:10.123456 UTC+0000"
        actual = utc_dt.strftime(self.fmt)
        self.assertEqual(expect,actual)
        nyc_dt = mdt.get_aware_datetime_from_epoch(epoch,"America/New_York")
        expect = "2019-05-14 14:30:10.123456 EDT-0400"
        actual = nyc_dt.strftime(self.fmt)
        self.assertEqual(expect,actual)

    def test_get_aware_datetime_from_naive(self):
        aware_dt1 = mdt.get_aware_datetime(2019, 5, 14, 18, 30, 10, 123456, "UTC")
        naive_dt  = mdt.get_naive_datetime(aware_dt1)
        aware_dt2 = mdt.get_aware_datetime_from_naive(naive_dt,"UTC")
        expect = "2019-05-14 18:30:10.123456 UTC+0000"
        actual = aware_dt2.strftime(self.fmt)
        self.assertEqual(expect,actual)
        aware_dt3 = mdt.get_aware_datetime_from_naive(naive_dt,"America/New_York")
        expect = "2019-05-14 18:30:10.123456 EDT-0400"  # tz changes, but time not converted
        actual = aware_dt3.strftime(self.fmt)
        self.assertEqual(expect,actual)

    def test_get_now_aware_datetime(self):
        utc_dt = mdt.get_now_aware_datetime("UTC")
        nyc_dt = mdt.get_now_aware_datetime("America/New_York")
        loc_dt = mdt.get_now_aware_datetime()
        self.assertEqual("UTC",str(utc_dt.tzinfo))
        self.assertEqual("America/New_York",str(nyc_dt.tzinfo))
        self.assertEqual(str(tzlocal.get_localzone()),str(loc_dt.tzinfo))

    def test_convert_aware_datetime(self):
        utc_dt = mdt.get_aware_datetime(2019, 5, 14, 18, 30, 10, 123456, "UTC")
        nyc_dt = mdt.convert_aware_datetime(utc_dt,"America/New_York")
        lax_dt = mdt.convert_aware_datetime(nyc_dt,"America/Los_Angeles")
        utc_expect = "2019-05-14 18:30:10.123456 UTC+0000"
        nyc_expect = "2019-05-14 14:30:10.123456 EDT-0400"
        lax_expect = "2019-05-14 11:30:10.123456 PDT-0700"
        utc_actual = utc_dt.strftime(self.fmt)
        nyc_actual = nyc_dt.strftime(self.fmt)
        lax_actual = lax_dt.strftime(self.fmt)
        self.assertEqual(utc_expect,utc_actual)
        self.assertEqual(nyc_expect,nyc_actual)
        self.assertEqual(lax_expect,lax_actual)

    def test_get_naive_datetime(self):
        the_dt = mdt.get_aware_datetime(2019, 5, 14, 18, 30, 10, 123456, "America/New_York")
        naive_dt = mdt.get_naive_datetime(the_dt)
        self.assertTrue(mdt.is_naive(naive_dt))
        self.assertEqual(  2019,naive_dt.year)
        self.assertEqual(     5,naive_dt.month)
        self.assertEqual(    14,naive_dt.day)
        self.assertEqual(    18,naive_dt.hour)
        self.assertEqual(    30,naive_dt.minute)
        self.assertEqual(    10,naive_dt.second)
        self.assertEqual(123456,naive_dt.microsecond)
        self.assertIsNone(naive_dt.tzinfo)

    def test_format_datetime(self):
        aware_dt = mdt.get_aware_datetime(2019, 5, 14, 18, 30, 10, 123456, "America/New_York")
        aware_dt_str = mdt.format_datetime(aware_dt)
        self.assertEqual("2019-05-14 18:30:10.123456 EDT-0400",aware_dt_str)
        aware_dt_str = mdt.format_datetime(aware_dt,precision=4)
        self.assertEqual("2019-05-14 18:30:10.1234 EDT-0400",aware_dt_str)
        aware_dt_str = mdt.format_datetime(aware_dt,precision=9)
        self.assertEqual("2019-05-14 18:30:10.123456000 EDT-0400",aware_dt_str)
        naive_dt = mdt.get_naive_datetime(aware_dt)
        aware_dt_str = mdt.format_datetime(aware_dt,precision=9,nanoseconds=123456789)
        self.assertEqual("2019-05-14 18:30:10.123456789 EDT-0400",aware_dt_str)
        aware_dt_str = mdt.format_datetime(aware_dt,precision=11,nanoseconds=123456789)
        self.assertEqual("2019-05-14 18:30:10.123456789 EDT-0400",aware_dt_str)
        aware_dt_str = mdt.format_datetime(aware_dt,precision=0,nanoseconds=123456789)
        self.assertEqual("2019-05-14 18:30:10. EDT-0400",aware_dt_str)
        aware_dt_str = mdt.format_datetime(aware_dt,precision=-1,nanoseconds=123456789)
        self.assertEqual("2019-05-14 18:30:10. EDT-0400",aware_dt_str)
        naive_dt_str = mdt.format_datetime(naive_dt)
        self.assertEqual("2019-05-14 18:30:10.123456 ",naive_dt_str)
        aware_dt_str = mdt.format_datetime(aware_dt,precision=8,nanoseconds=987654321)
        self.assertEqual("2019-05-14 18:30:10.98765432 EDT-0400",aware_dt_str)

if __name__=='__main__':
    unittest.main()
