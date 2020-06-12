"""Defnes the MotleyFormatter class to extend formatting features (especially datetime related) for log messages."""
import logging
import pytz
from datetime import datetime
import re
import motleylog.motleydatetime as mdt
class MotleyFormatter(logging.Formatter):
    """A subclass of "logging.Formatter" which extends/simplifies datetime related logging issues.

    A class which facilitates creation of extended formats for the standard "logging" module (and also
    for the extemded motleylogger module). Primarilly makes proper inclusion of high resolution datetimes
    in log messages easy (up to nanosecond resolution on modern systems). Also makes it easier to use UTC
    or any other desired timezone in log messages. The MotleyFormatter class is a subclass of the
    standard logging.Formatter class so no standard logging format features should be lost.

    See the standard logging.Formatter documentation for more details.

    Attributes:
        fmt (str): The log formatting string.
        style (str) : The log formatting string substitution style ('%',, '{', or '$'.
        datefmt (str) : The strftime-stype datetime formatting string.
        tzstr (str) : The name of the timezone desired for datetimes.
        precision (int) : Number of digits displayed when expanding the '%f' part of datefmt.
    """

    def __init__(self, fmt='%(levelname)s: %(asctime)s: %(message)s', style='%',
                 datefmt='%Y-%m-%d %H:%M:%S.%f %Z%z', tzstr='UTC', precision=6):
        """Initializes the class and create a formatter instance with the specified characteristics.

        Parameters:
            fmt (str) : Specifies the overall format of the log message. Can be specified in '%', '{', or '$'
                substitution styles but must match the style identified by the 'style' parameter (see below).
                Refer to documentation for the standard 'logging' module for more details.
            style (str) : Specifies the sunstitution style used by the 'fmt' parameter above.
                Must be '%', '{', or '$'.
            datefmt (str) : Specifies the datetime formatting to be used for the %(asctime) portion of the
                log message (if included). These datatime formatting rules are defined in the
                'datetime.datetime.strftime' method; refer to detailed documentation there.
            tzstr (str) : A valid timezone name. If %(asctime) is included in the log message than all datetime
                will be converted to this timezone. In general it is recommended to use the "UTC" timezone
                (Coordinated Universal Time) for log messages. A list of all valid timezones can be printed
                using the 'pytz' module and printing the pytz.all_timezones list. Your computer's current
                local timezone can be specified using 'tzstr=str(tzlocal.get_localzone())'.
            precision (int) : Specifies the desired number of digits of fractional seconds in log message datetimes.
                This applies only if %(asctime) is included in the "fmt" parameter and "%f% in included somewhete
                in the "datefmt" parameter. The default is precision=6 which uses 6 decimal digits (zero-filled)
                to indicates microseconds as the fractional part. For nanosecond resolution (if your system
                supports it) precision=9 can be specified. Using precision=3 displays milliseconds for the
                fractional part. The value of the precision parameter, if specified, is restricted to be
                from 0 to 9 inclusive.
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
        """Formats the datetime (asctime) portion of a log message.

        This method overrides the base "formatTime" method in the "logging.Formatter" class.

        Parameters:
            loggingRecord (logging.LogRecord) : The unformatted log record object which must be an instance of
                logging.LogRecord.
            datefmt (str) : The "datetime.datetime.strftime" style format string which determines how a datetime
                is formatted. Works just like standard strftime formatting except that the microsecond expansion
                of "%f" which is normally six zero-filled decimal digits can be altered to be from 0 to 9 digits
                long depending on the value of the "precision" parameter when the containing motleyFormatter
                class was instantiated. If datefmt is not specified here, the class instance "datefmt" attribute
                is used as a default.

        Returns:
           str : The formatted datetime as a string.
        """
        aware_dt = mdt.get_aware_datetime_from_epoch(loggingRecord.created,self.timezone)
        nanoseconds = int(loggingRecord.msecs * 1000000)
        formatted_datetime = mdt.format_datetime(aware_dt,self.datefmt,self.precision,nanoseconds)
        return formatted_datetime

    def get_fmt(self):
        """Gets the log message formating string for the instance.

        Returns:
            str : The log message formatting string.
        """
        return self.fmt

    def set_fmt(self, fmt='%(levelname)s: %(asctime)s: %(message)s'):
        """Sets the log message formatting string.

        Parameters:
            fmt (str) : The log message formatting string.
        """
        self.fmt = fmt

    def get_style(self):
        """Gets the log message formating style indicating character.

        Returns:
            str : The log message formatting string substitution style, "%", "{", or "$".
        """
        return self.style

    def set_style(self, style='%'):
        """Sets the log message formatting string.

        Must be '%',. '{', or '$' to indicate the formatting string substitution style.

        Parameters:
            style (str) : The log message formatting string.
        """
        self.style = style

    def get_datefmt(self):
        """Gets the strftime-style datetime formatting string.

        Returns:
            str : The the strftime-style datetime formatting string.
        """
        return self.datefmt

    def set_datefmt(self, datefmt='%Y-%m-%d %H:%M:%S.%f %Z%z'):
        """Sets the strftime-style datetime formatting string.

        Parameters:
            datefmt (str) : The strftime-style datetime formatting string.
        """
        self.datefmt = datefmt

    def get_tzstr(self):
        """Gets the timezone name string used for datetimes.

        Returns:
            str : The timezone name string used for datetimes.
        """
        return self.tzstr

    def set_tzstr(self,tzstr='UTC'):
        """Sets the timezone used for datetimes.

        Parameters:
            tzstr (str) : The timezone name string (as in pytz.all_timezones). To specify your computer
                local timezone specify "tzstr=str(tzlocal.get_localzone())".
        """
        self.timezone  = pytz.timezone(tzstr)
        self.tzstr = tzstr

    def get_precision(self):
        """Gets the number of digits (0 through 9) used when expanding '%f' in a datetime formatting string.

        Returns:
            int : The number of digits (0 through 9) used when expanding '%f' in a datetime formatting string.
        """
        return self.precision

    def set_precision(self, precision):
        """Sets the number of digits (0 through 9) used when expanding '%f' in a datetime formatting string.

        Parameters:
            precision (int) : The number of digits (0 through 9) used when expanding '%f' in a datetime
                formatting string.
        """
        precision = min(9, max(0, int(precision)))
        self.precision = precision
