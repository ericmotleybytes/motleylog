import logging
from datetime import datetime
import re
import motleylog.motleydatetime as motleydatetime
class MotleyFormatter(logging.Formatter):

    #def __init__(self, fmt=None, datefmt=None, style='%', utc=True):
    def __init__(self, fmt=None, datefmt=None, style='%', tz="UTC"):
        #self.utcFlag = bool(utc)
        if tz=="UTC" or tz=="utc":
            self.utcFlag = True
        else:
            self.utcFlag = False
        self.fmt = fmt
        if self.fmt is None:
            self.fmt = '%(levelname)s: %(asctime)s:  %(message)s'
        self.datefmt = datefmt
        self.f_re = re.compile('%f\d')
        if datefmt is None:
            self.datefmt = "%Y-%m-%d %H:%M:%S.%f %z"
        super().__init__(fmt=self.fmt,datefmt=self.datefmt, style='%')
        if self.utcFlag:
            self.converter = datetime.utcfromtimestamp
        else:
            self.converter = datetime.fromtimestamp

    def formatTime(self, loggingRecord, datefmt=None):
        epochSeconds = loggingRecord.created   # epoch seconds as integer
        ct = self.converter(loggingRecord.created)  # epoch seconds in, datetime out
        if datefmt is None:
            datefmt = self.datefmt  # instance setting
        # substitute timezone for %z if present
        if datefmt.find('%z')>=0:
            if self.utcFlag:
                timeZoneStr = "+0000"
            else:
                timeZoneStr = motleydatetime.getLocalTzOffset()  # timezone as '+HHMM' or '-HHMM'
            datefmt = datefmt.replace('%z',timeZoneStr)
        # substitute fractional second part for %f[n]
        milliSecs = loggingRecord.msecs  # float number of milliseconds
        nanoSecs = int(milliSecs * 1000000)
        nanoSecsStr = '%09d' % (nanoSecs,)
        for prec in range(0,10):
            placeholder = f'%f{prec}'
            if datefmt.find(placeholder):
                datefmt = datefmt.replace(placeholder, nanoSecsStr[0:prec])
        placeholder = f'%f'
        if datefmt.find(placeholder):
            datefmt = datefmt.replace(placeholder, nanoSecsStr[0:6])
        dtStr = ct.strftime(datefmt)
        return dtStr  # formatted datetime string

    def getfmt(self):
        return self.fmt

    def getdatefmt(self):
        return self.datefmt

    def getutc(self):
        return self.utcFlag
