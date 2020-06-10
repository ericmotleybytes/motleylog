"""Defnes the MotleyFormatter class to extend formatting features (especially datetime related) for log messages."""
import logging
import pytz
from datetime import datetime
import re
import motleylog.motleydatetime as mdt
class MotleyFormatter(logging.Formatter):
    """A subclass of "logging.Formatter" which extends/simplifies datetime related logging issues.

    A class which facilitates creation of extended formats for the standard "logging" module (and also
    for the extemded motleylogger module). Primarilly makes inclusion of high resolution datetimes in
    log messages easy (up to nanosecond resolution on modern systems). Also makes it easier to use UTC
    or any other desired timezone in log messages. The MotleyFormatter class is a subclass of the
    standard logging.Formatter class so no standard logging format features should be lost.

    See the standard logging.Formatter documentation for more details.
    """

    def __init__(self, fmt='%(levelname)s: %(asctime)s: %(message)s', style='%',
                 datefmt='%Y-%m-%d %H:%M:%S.%f %Z%z', tzstr='UTC', precision=6):
        """Initializes the class and create a formatter instance with the specified characteristics.

        Parameters
        ----------
        fmt : str
            Specifies the overall format of the log message. Can be specified in '%', '{', or '$'
            substitution styles but must match the style identified by the 'style' parameter (see below).
            Refer to documentation for the standard 'logging' module for more details.

        style : str
            Specifies the sunstitution style used by the 'fmt' parameter above. Must be '%', '{', or '$'.

        datefmt : str
            Specifies the datetime formatting to be used for the %(asctime) portion of the log message (if
            included). These datatime formatting rules are defined in the 'datetime.datetime.strftime'
            method, refer to detailed documentation there.

        tzstr : str
            A valid timezone name. If %(asctime) is included in the log message than all datetime will be
            converted to this timezone. In general it is recommended to use the "UTC" timezone (Coordinated
            Universal Time) for log messages. A list of all valid timezones can be printed using the
            'pytz' module and printing the pytz.all_timezones list. Your computer's current local timezone
            can be obtained using the 'tzlocal.get_localzone()' function.

        precision : int
            Specifies the desisred precision of frational seconds in log message datetimes. This allies only
            if %(asctime) is included in the "fmt" parameter and "%f% in included somewhete in the datefmt
            parameter. The default is to precision=6 which uses 6 decimal digits (zero-filled) to indicates
            microseconds as the fractional part. For nanosecond resolution (if your system support it)
            precision=9 can be specified. Using precision=3 displays milliseconds for the fractional part.
            The value of the precision parameter, if specified, must be from 0 to 9 inclusive.
        """
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
