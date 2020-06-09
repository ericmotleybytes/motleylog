import logging
import pytz
from datetime import datetime
import re
import motleylog.motleydatetime as mdt
class MotleyFormatter(logging.Formatter):

    def __init__(self, fmt='%(levelname)s: %(asctime)s: %(message)s', style='%',
                 datefmt='%Y-%m-%d %H:%M:%S.%f %Z%z', tzstr='UTC', precision=6):
        self.fmt = fmt
        if self.fmt is None:
            self.fmt = '%(levelname)s: %(asctime)s:  %(message)s'
        self.style     = style
        self.datefmt   = datefmt
        self.tzstr     = tzstr
        self.timezone  = pytz.timezone(tzstr)
        self.precision = min(9,max(0,int(precision)))
        super().__init__(fmt=self.fmt,datefmt=self.datefmt, style=self.style)

    def formatTime(self, loggingRecord, datefmt=None):
        # overrides same name method in superclass
        epochSeconds = loggingRecord.created    # epoch seconds as integer or float
        milliSecs = loggingRecord.msecs       # float number of milliseconds
        microSecs = int(milliSecs * 1000)     # int number of microseconds
        nanoSecs  = int(milliSecs * 1000000)  # int number of nanoseconds
        if isinstance(epochSeconds,int):
            adjEpoch   = float(epochSeconds) + (milliSecs / 1000.0)
        else:
            adjEpoch   = epochSeconds
        record_dt = mdt.get_aware_datetime_from_epoch(adjEpoch,self.timezone)
        if datefmt is None:
            datefmt = self.datefmt  # instance setting
        if self.precision != 6:
            if datefmt.find('%f')>=0:
                digits = '%09d' % nanoSecs
                digits = digits[0:self.precision]
                datefmt = datefmt.replace('%f',digits)
        formatted_datetime = record_dt.strftime(datefmt)
        return formatted_datetime  # formatted datetime string

    def format(self, loggingRecord):
        #print(loggingRecord)
        #for k,v in loggingRecord.__dict__.items():
        #    print(k,"=",v)
        result = super().format(loggingRecord)
        return result

    def get_fmt(self):
        return self.fmt

    def get_style(self):
        return self.style

    def get_datefmt(self):
        return self.datefmt

    def get_timezone(self):
        return self.timezone

    def get_tzstr(self):
        return self.tzstr

    def get_precision(self):
        return self.precision

    #def getutc(self):
    #    return self.utcFlag
