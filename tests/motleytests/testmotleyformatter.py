import unittest
import unittest.mock
import logging
import sys
import io
import pytz
import motleylog.motleydatetime as mdt
import motleylog.motleyformatter as mf
class TestMotleyFormatter(unittest.TestCase):
    def setup(self):
        # Executed before each test method.
        # Get a fresh logger.
        if "loggerCount" not in self.__dict__:
            self.loggerCount = 1
        else:
            self.loggerCount = self.loggerCount + 1
        loggerName = f'{__name__}_{self.loggerCount}'
        self.logger = logging.getLogger(loggerName)
        self.logger.setLevel(logging.DEBUG)
        self.formatter = logging.Formatter(fmt='%(levelname)s: %(asctime)s: %(message)s',style='%',
                                           datefmt='%Y-%m-%d %H:%M:%S.%f %Z%z')
        self.handler = logging.StreamHandler(sys.stdout)
        self.handler.setFormatter(self.formatter)
        self.handler.setLevel(logging.DEBUG)
        self.logger.addHandler(self.handler)

    def test_set_get_fmt(self):
        f1 = mf.MotleyFormatter()
        self.assertEqual('%(levelname)s: %(asctime)s: %(message)s',f1.get_fmt())
        f1.set_fmt('%(levelname)s: %(message)s')
        self.assertEqual('%(levelname)s: %(message)s', f1.get_fmt())

    def test_set_get_style(self):
        f1 = mf.MotleyFormatter()
        self.assertEqual('%',f1.get_style())
        f1.set_style('$')
        self.assertEqual('$', f1.get_style())

    def test_set_get_datefmt(self):
        f1 = mf.MotleyFormatter()
        self.assertEqual('%Y-%m-%d %H:%M:%S.%f %Z%z',f1.get_datefmt())
        f1.set_datefmt('%Y-%m-%d %H:%M:%S %Z')
        self.assertEqual('%Y-%m-%d %H:%M:%S %Z', f1.get_datefmt())

    def test_set_get_tzstr(self):
        f1 = mf.MotleyFormatter()
        self.assertEqual('UTC',f1.get_tzstr())
        f1.set_tzstr('America/New_York')
        self.assertEqual('America/New_York', f1.get_tzstr())
        try:
            f1.set_tzstr('Not a timezone.')
        except pytz.exceptions.UnknownTimeZoneError:
            self.assertTrue(True,"Expected exception caught.")
        except:
            self.fail("Unexpected exception: " + sys.exc_info()[0])

    def test_set_get_precision(self):
        f1 = mf.MotleyFormatter()
        self.assertEqual(6,f1.get_precision())
        f1.set_precision(9)
        self.assertEqual(9, f1.get_precision())
        f1.set_precision(0)
        self.assertEqual(0, f1.get_precision())
        f1.set_precision(42)
        self.assertEqual(9, f1.get_precision())  # precision limited
        f1.set_precision(-1)
        self.assertEqual(0, f1.get_precision())  # precision limited
        f1.set_precision(5.7)
        self.assertEqual(5, f1.get_precision())  # precision limited
        f1.set_precision('3')
        self.assertEqual(3, f1.get_precision())  # precision limited
        try:
            f1.set_precision('4')
            f1.set_precision('two')
            self.assertEqual(4, f1.get_precision())
        except ValueError:
            self.assertTrue(True,"Expected exception caught.")
        except:
            self.fail("Unexpected exception: " + sys.exc_info()[0])

    def test_formatTime(self):
        # Get a fresh logger.
        #loggerName = __name__ + 'test_formatTime'
        #logger = logging.getLogger(loggerName)
        #logger.setLevel(logging.DEBUG)
        #formatter = logging.Formatter(fmt='%(asctime)s', style='%', datefmt='%Y-%m-%d %H:%M:%S.%f %Z%z')
        #handler = logging.StreamHandler(sys.stdout)
        #handler.setFormatter(self.formatter)
        #handler.setLevel(logging.DEBUG)
        #logger.addHandler(self.handler)
        #with unittest.mock.patch('sys.stdout', new=io.StringIO()) as outbuf:
        #    logger.debug("dummy")
        #self.assertEqual("",outbuf.getvalue().strip())
        #
        aware_dt = mdt.get_aware_datetime(2019, 5, 14, 18, 30, 10, 123456, "UTC")
        ts = mdt.get_epoch_from_aware_datetime(aware_dt)
        log_record = logging.LogRecord("loggername",logging.DEBUG,pathname="/home",lineno=0,msg="dummy",
                                       args=None,exc_info=None)
        log_record.created = ts
        log_record.msecs = 123456/1000.0
        f1 = mf.MotleyFormatter()
        expect = "2019-05-14 18:30:10.123456 UTC+0000"
        actual = f1.formatTime(log_record,None)
        self.assertEqual(expect,actual)
        #
        aware_dt = mdt.get_aware_datetime(2019, 5, 14, 18, 30, 10, 123456, "UTC")
        ts = mdt.get_epoch_from_aware_datetime(aware_dt)
        log_record = logging.LogRecord(
                "loggername",logging.DEBUG,pathname="/home",lineno=0,msg="dummy",
                 args=None,exc_info=None)
        log_record.created = ts
        nanoseconds = 987654321
        milliseconds = nanoseconds/1000000.0
        log_record.msecs = milliseconds
        f1 = mf.MotleyFormatter()
        f1.set_precision(4)
        expect = "2019-05-14 18:30:10.9876 UTC+0000"
        actual = f1.formatTime(log_record,None)
        self.assertEqual(expect,actual)
        #
        aware_dt = mdt.get_aware_datetime(2019, 5, 14, 18, 30, 10, timezone="UTC")
        ts = mdt.get_epoch_from_aware_datetime(aware_dt)
        log_record = logging.LogRecord("loggername", logging.DEBUG, pathname="/home", lineno=0, msg="dummy",
                                       args=None, exc_info=None)
        log_record.created = ts
        log_record.msecs = 123456 / 1000.0
        f1 = mf.MotleyFormatter()
        expect = "2019-05-14 18:30:10.123456 UTC+0000"
        actual = f1.formatTime(log_record, None)
        self.assertEqual(expect, actual)

if __name__=='__main__':
    unittest.main()
