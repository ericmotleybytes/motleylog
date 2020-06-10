"""Programming support libraries.

The modules in this package

Module Summary
--------------
    motleydatetime
        Makes datetime manipulation easy and reliable. Potentially useful to any Python program
        which uses the standard "datetime" module, especially when dealing with timezones or UTC datetimes.

    motleyformatter
        Implements the MotleyFormatter class which facilitates creation of extended formats for the
        standard "logging" module (and also for the extemded motleylogger module). Primarilly makes
        inclusion of high resolution datetimes in log messages easy (up to nanosecond resolution on
        modern systems). Also makes it easier to use UTC or any other desired timezone in log messages.
        The MotleyFormatter class is a subclass of the standard logging.Formatter class so no standard
        logging format features should be lost.

    motleylogger
        Implements the MotleyLogger class which extends the logging capabilities of the standard "logging"
        module. For technical reasons, MotleyLogger is not a subclass of "logging.Logger" class but
        transparently wraps most standard Logger methods to make usage easy for those who know standard
        logging methods. Some additional methods have also been added.
"""
