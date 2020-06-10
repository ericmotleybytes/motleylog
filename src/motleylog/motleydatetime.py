"""Functions to make datetime manipulation easy, accurate, and reliable."""
import sys
import time
import pytz
import tzlocal
import datetime

def is_naive(the_datetime):
    """Tests if a datetime.datetime object is 'naive', i.e., has no associated timezone information.

    See also is_aware.

    Parameters
    ----------
    the_datetime : datetime.datetime
        The datetime to be tested.

    Returns
    -------
    bool
        False if the_datetime has timezone information, True if it does not.

    Raises
    ------
    TypeError
        Raised if the_datetime parameter is not an instance of datetime.datetime.
    """
    if not isinstance(the_datetime,datetime.datetime):
        raise TypeError("Parameter the_datetime is not an instance of datetime.datetime.")
    if the_datetime.tzinfo is None:
        return True
    else:
        return False

def is_aware(the_datetime):
    """Tests if a datetime.datetime object is 'aware', i.e., has associated timezone information.

    See also is_naive.

    Parameters
    ----------
    the_datetime : datetime.datetime
        The datetime to be tested.

    Returns
    -------
    bool
        True if the_datetime has timezone information, False if it does not.

    Raises
    ------
    TypeError
        Raised if the_datetime parameter is not an instance of datetime.datetime.
    """
    if not isinstance(the_datetime,datetime.datetime):
        raise TypeError("Parameter the_datetime is not an instance of datetime.datetime.")
    if the_datetime.tzinfo is None:
        return False
    else:
        return True

def get_utc_datetime(year,month,day,hour=0,minute=0,second=0,microsecond=0):
    """Returns an aware datetime.datetime object with the specified datetime and associated with UTC timezone.

    Parameters
    ----------
    year : int
        The desired year, e.g., 2020.
    month : int
        The desired month number, 1 through 12, e.g., 1 for January and 12 for December.
    day : int
        The desired day of month, e.g., 25.
    hour : int
        The desired hour, 0 through 23, e.g., 14 for 2 p.m.
    minute : int
        The desired minute, 0 through 59, e.g., 33.
    second : int
        The desired second, 0 through 59, e.g., 45. Leap seconds generally ignored.
    microsecond : int
        The desired microsecond, 0 through 999999, e.g., 123456.

    Returns
    -------
    datetime.datetime
        An aware datetime.datetime object associated with timezone UTC and with the specified date and time values.

    Exceptions
    ----------
    TypeError
        Raised if any parameters not of an acceptable type.
    ValueError
        Raised if any values outside of valid ranges.
    """
    if not isinstance(year,int):
        raise TypeError("Parameter year is not an int.")
    if not isinstance(month,int):
        raise TypeError("Parameter month is not an int.")
    if not isinstance(day,int):
        raise TypeError("Parameter day is not an int.")
    if not isinstance(hour,int):
        raise TypeError("Parameter hour is not an int.")
    if not isinstance(minute,int):
        raise TypeError("Parameter minute is not an int.")
    if not isinstance(second,int):
        raise TypeError("Parameter second is not an int.")
    if not isinstance(microsecond,int):
        raise TypeError("Parameter microsecond is not an int.")
    tz_utc = pytz.utc
    dt_utc = tz_utc.localize(datetime.datetime(year,month,day,hour,minute,second,microsecond))
    return dt_utc

def get_aware_datetime(year,month,day,hour=0,minute=0,second=0,microsecond=0,timezone=tzlocal.get_localzone()):
    """Returns an aware datetime.datetime object with the specified datetime and associated with specified timezone.

    Parameters
    ----------
    year : int
        The desired year, e.g., 2020.
    month : int
        The desired month number, 1 through 12, e.g., 1 for January and 12 for December.
    day : int
        The desired day of month, e.g., 25.
    hour : int
        The desired hour, 0 through 23, e.g., 14 for 2 p.m.
    minute : int
        The desired minute, 0 through 59, e.g., 33.
    second : int
        The desired second, 0 through 59, e.g., 45. Leap seconds generally ignored.
    microsecond : int
        The desired microsecond, 0 through 999999, e.g., 123456.
    timezone : str or datetime.tzinfo (includes subclass pytz.timezone).
        Either a valid timezone name as a string, or a timezone object, usually a pytz.timezone object
        which is a child class of datetime.tzinfo.

    Returns
    -------
    datetime.datetime
        An aware datetime.datetime object associated with timezone UTC and with the specified date and time values.

    Exceptions
    ----------
    TypeError
        Raised if any parameters not of an acceptable type.
    ValueError
        Raised if any values outside of valid ranges.
    pytz.exceptions.UnknownTimeZoneError
        Raised is a string timezone name is not recognized.
    """
    if not isinstance(year,int):
        raise TypeError("Parameter year is not an int.")
    if not isinstance(month,int):
        raise TypeError("Parameter month is not an int.")
    if not isinstance(day,int):
        raise TypeError("Parameter day is not an int.")
    if not isinstance(hour,int):
        raise TypeError("Parameter hour is not an int.")
    if not isinstance(minute,int):
        raise TypeError("Parameter minute is not an int.")
    if not isinstance(second,int):
        raise TypeError("Parameter second is not an int.")
    if not isinstance(microsecond,int):
        raise TypeError("Parameter microsecond is not an int.")
    if timezone.__class__.__name__ == "str":
        timezone = pytz.timezone(timezone)
    elif not isinstance(timezone,datetime.tzinfo):
        raise TypeError("Parameter timezone is not a timezone name or an instance of datetime.tzinfo.")
    aware_dt = timezone.localize(datetime.datetime(year,month,day,hour,minute,second,microsecond))
    return aware_dt

def get_epoch_from_aware_datetime(aware_datetime):
    """Returns number of seconds (including fractions) from the epoch base instant to aware_datetime instant.

    Parameters
    ----------
    aware_datetime : datetime.datetime
        A timezone aware datetime.datetime object.

    Returns
    -------
    datetime.datetime
        An aware datetime.datetime object associated with timezone UTC and with the specified date and time values.

    Raises
    ------
    TypeError
        Raised if any parameters not of an acceptable type.
    RunTimeError
        Raised if paraneter aware_datetime is naive, not aware.
    """
    if is_naive(aware_datetime):
        raise RuntimeError("Datetime parameter is not timezone aware.")
    base_epoch = datetime.datetime.utcfromtimestamp(0).replace(tzinfo=pytz.utc)
    dt_epoch = (aware_datetime - base_epoch).total_seconds()   # fractional seconds
    return dt_epoch

def get_utc_datetime_from_epoch(epoch=time.time()):
    """Returns a UTC timezone aware datetime.datetime set from the epoch seconds (including fractions).

    Parameters
    ----------
    epoch : float
        Number of seconds (including fractions) since system epoch. Can also be an int.

    Returns
    -------
    datetime.datetime
        An aware datetime.datetime object associated with timezone UTC and with the equivalent date and time values.

    Raises
    ------
    TypeError
        Raised if any parameters not of an acceptable type.
    """
    if not isinstance(epoch,int) and not isinstance(epoch,float):
        raise TypeError("Epoch parameter is not an int or a float.")
    aware_dt = datetime.datetime.fromtimestamp(epoch,pytz.utc)
    return aware_dt

def get_aware_datetime_from_epoch(epoch=time.time(),timezone=tzlocal.get_localzone()):
    """Returns a datetime.datetime set from the epoch seconds and aware of specified timezone.

    Parameters
    ----------
    epoch : float
        Number of seconds (including fractions) since system epoch. Can also be an int.
    timezone : str or datetime.tzinfo (includes subclass pytz.timezone).
        Either a valid timezone name as a string, or a timezone object, usually a pytz.timezone object
        which is a child class of datetime.tzinfo.

    Returns
    -------
    datetime.datetime
        An aware datetime.datetime object associated with specified timezone and with the equivalent datetime values.

    Raises
    ------
    TypeError
        Raised if any parameters not of an acceptable type.
    """
    if not isinstance(epoch,int) and not isinstance(epoch,float):
        raise RuntimeError("Epoch parameter is an int or a float.")
    if timezone.__class__.__name__ == "str":
        timezone = pytz.timezone(timezone)
    elif not isinstance(timezone,datetime.tzinfo):
        raise TypeError("Parameter timezone is not a timezone name or an instance of datetime.tzinfo.")
    aware_dt = datetime.datetime.fromtimestamp(epoch,timezone)
    return aware_dt

def get_aware_datetime_from_naive(naive_datetime,timezone=tzlocal.get_localzone()):
    """Returns a localized (made timezone aware) datetime.datetime but does not convert any date or time values.

    Parameters
    ----------
    naive_datetime : datetime.datetime
        A naive datetime.datetime object (not internally associated with any timezone).
    timezone : str or datetime.tzinfo (includes subclass pytz.timezone).
        Either a valid timezone name as a string, or a timezone object, usually a pytz.timezone object
        which is a child class of datetime.tzinfo.

    Returns
    -------
    datetime.datetime
        An datetime.datetime object aware of the specified timezone.

    Raises
    ------
    TypeError
        Raised if any parameters not of an acceptable type.
    RunTimeError
        Raised if naive_datetime parameter not naive but is rather timezone aware.
    """
    # Localized naive datetime, but no timezone conversion performed.
    if is_aware(naive_datetime):
        raise RuntimeError("Naive datetime parameter is not naive.")
    if timezone.__class__.__name__ == "str":
        timezone = pytz.timezone(timezone)
    elif not isinstance(timezone,datetime.tzinfo):
        raise TypeError("Parameter timezone is not a timezone name or an instance of datetime.tzinfo.")
    aware_dt = timezone.localize(naive_datetime)
    return aware_dt

def get_now_aware_datetime(timezone=tzlocal.get_localzone()):
    """Returns a timezone aware datetime of the current date and time in the specified timezone.

    Parameters
    ----------
    timezone : str or datetime.tzinfo (includes subclass pytz.timezone).
        Either a valid timezone name as a string, or a timezone object, usually a pytz.timezone object
        which is a child class of datetime.tzinfo.

    Returns
    -------
    datetime.datetime
        An datetime.datetime object with current datetime in the specified timezone.

    Raises
    ------
    TypeError
        Raised if any parameters not of an acceptable type.
    """
    if timezone.__class__.__name__ == "str":
        timezone = pytz.timezone(timezone)
    elif not isinstance(timezone,datetime.tzinfo):
        raise TypeError("Parameter timezone is not a timezone name or an instance of datetime.tzinfo.")
    epoch = time.time()
    aware_dt = datetime.datetime.fromtimestamp(epoch,timezone)
    return aware_dt

def convert_aware_datetime(old_aware_datetime,timezone=tzlocal.get_localzone()):
    """Converts a timezone aware datetime into another datetime aware of another timezone.

    Parameters
    ----------
    old_aware_datetime : datetime.datetime
        A timezone aware datetime.
    timezone : str or datetime.tzinfo (includes subclass pytz.timezone).
        Either a valid timezone name as a string, or a timezone object, usually a pytz.timezone object
        which is a child class of datetime.tzinfo.

    Returns
    -------
    datetime.datetime
        An datetime.datetime object aware of the new timezone and with properly converted date and time values.

    Raises
    ------
    RunTimeError
        Raised if old_aware_datetime parameter is not aware of any timezone.
    TypeError
        Raised if any parameters not of an acceptable type.
    """
    if is_naive(old_aware_datetime):
        raise RuntimeError("Datetime parameter is not timezone aware.")
    if timezone.__class__.__name__ == "str":
        timezone = pytz.timezone(timezone)
    elif not isinstance(timezone,datetime.tzinfo):
        raise TypeError("Parameter timezone is not a timezone name or an instance of datetime.tzinfo.")
    new_aware_datetime = old_aware_datetime.astimezone(timezone)
    return new_aware_datetime

def get_naive_datetime(old_aware_datetime):
    """Converts a timezone aware datetime into a naive datetime with same date and time values.

    Parameters
    ----------
    old_aware_datetime : datetime.datetime
        Preferably a timezone aware datetime, but might redundantly also be a naive datetime.

    Returns
    -------
    datetime.datetime
        An datetime.datetime object not aware (naive) of any timezone and with the same date and time values.

    Raises
    ------
    TypeError
        Raised if any parameters not of an acceptable type.
    """
    if not isinstance(old_aware_datetime,datetime.datetime):
        raise TypeError("Parameter old_aware_datetime is not an instance of datetime.datetime.")
    new_naive_datetime = old_aware_datetime.replace(tzinfo=None)
    return new_naive_datetime
