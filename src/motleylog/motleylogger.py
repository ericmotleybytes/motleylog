import sys
import logging
from motleylog.motleyformatter import MotleyFormatter
class MotleyLogger(object):
    DEFAULT_LOGGER_NAME  = "MOTLEYLOG"  # Default name for logger.
    motleyLoggers        = {}           # All MotleyLogger instances stored in this dict.
    # wrap logging constants
    DEBUG    = logging.DEBUG
    NOTSET   = logging.NOTSET
    CRITICAL = logging.CRITICAL
    ERROR    = logging.ERROR
    FATAL    = logging.FATAL
    INFO     = logging.INFO
    WARNING  = logging.WARNING

    def __init__(self, loggerName=None):
        # Note: Do initializations of new instance in __new__ not here in __init__!
        pass

    def __new__(cls, loggerName = None):
        # Provide a default logger name not explicitly specified.
        if loggerName is None:
            loggerName = MotleyLogger.DEFAULT_LOGGER_NAME
        else:
            loggerName = str(loggerName)   # Make sure name is a string.
        # retieve or create new instance
        if loggerName in MotleyLogger.motleyLoggers:
            instance = MotleyLogger.motleyLoggers[loggerName]  # get saved instance
        else:
            instance = object.__new__(cls)
            instance.motleyLoggerName = loggerName
            if loggerName in logging.Logger.manager.loggerDict:
                # logging.Logger already exists, no need to initialize
                instance.loggingLogger = logging.getLogger(loggerName)
            else:
                # logging.Logger is new, initialize
                instance.loggingLogger = logging.getLogger(loggerName)
                instance.loggingLogger.setLevel(logging.DEBUG)
                formatter = MotleyFormatter()
                consoleHandler = logging.StreamHandler(sys.stdout)
                consoleHandler.setFormatter(formatter)
                instance.loggingLogger.addHandler(consoleHandler)
            # save MotleyLogger instance in master dictionary
            MotleyLogger.motleyLoggers[loggerName] = instance
        return instance

    @classmethod
    def getLogger(cls,loggerName=None):
        if loggerName is None:
            loggerName = MotleyLogger.DEFAULT_LOGGER_NAME
        else:
            loggerName = str(loggerName)
        if loggerName in MotleyLogger.motleyLoggers:
            logger = MotleyLogger.motleyLoggers[loggerName]
        else:
            logger = cls.__new__(cls,loggerName=loggerName)
        return logger

    @staticmethod
    def removeLogger(name=None):
        if name is None:
            name = MotleyLogger.DEFAULT_LOGGER_NAME
            return None
        if name in MotleyLogger.motleyLoggers:
            return MotleyLogger.motleyLoggers.pop(name)

    def getLoggingLogger(self):
        return self.loggingLogger

    def getMotleyLoggerName(self):
        return self.motleyLoggerName

    def getLoggingLoggerName(self):
        return self.loggingLogger.name

    def getLoggingLogger(self):
        return self.loggingLogger

    # Define wrapper methods for primary logging.logger methods.
    def addHandler(self, hdlr):
        return self.loggingLogger.addHandler(hdlr)
    def callHandlers(self, record):
        return self.loggingLogger.callHandlers(record)
    def critical(self,msg, *args, **kwargs):
        return self.loggingLogger.critical(msg, *args, **kwargs)
    def debug(self, msg, *args, **kwargs):
        return self.loggingLogger.debug(msg, *args, **kwargs)
    def error(self, msg, *args, **kwargs):
        return self.loggingLogger.error(msg, *args, **kwargs)
    def exception(self, msg, *args, exc_info=True, **kwargs):
         return self.loggingLogger.error(msg, *args, exc_info=exc_info, **kwargs)
    def fatal(self, msg, *args, **kwargs):
        return self.loggingLogger.fatal(msg, *args, **kwargs)
    def findCaller(self, stack_info=False, stacklevel=2):
        return self.loggingLogger.findCaller(stack_info=stack_info, stacklevel=stacklevel)
    def getChild(self,suffix):
        return self.loggingLogger.getChild(suffix)
    def getEffectiveLevel(self):
        return self.loggingLogger.getEffectiveLevel()
    def handle(self, record):
        return self.loggingLogger.handle(record)
    def hasHandlers(self):
        return self.loggingLogger.hasHandlers()
    def info(self, msg, *args, **kwargs):
        return self.loggingLogger.info(msg, *args, **kwargs)
    def isEnabledFor(self, level):
        return self.loggingLogger.isEnabledFor(level)
    def log(self, level, msg, *args, **kwargs):
        return self.loggingLogger.log(level, msg, *args, **kwargs)
    def makeRecord(self, name, level, fn, lno, msg, args, exc_info, func=None, extra=None, sinfo=None):
        return self.loggingLogger.makeRecord(name,level,fn,lno,msg,args,exc_info,func=func,extra=extra,sinfo=sinfo)
    def removeHandler(self, hdlr):
        return self.loggingLogger.removeHandler(hdlr)
    def setLevel(self, level, all=True):
        if all:
            for hdlr in self.loggingLogger.handlers:
                hdlr.setLevel(level)
        return self.loggingLogger.setLevel(level)
    def warning(self, msg, *args, **kwargs):
        return self.loggingLogger.warning(msg, *args, **kwargs)
    def addFilter(self, filter):
        return self.loggingLogger.addFilter(filter)
    def filter(self, record):
        return self.loggingLogger.filter(record)
    def removeFilter(self, filter):
        return self.loggingLogger.removeFilter(filter)

    # more extensions
    def getHandlerList(self):
        result = []
        for hdlr in self.loggingLogger.handlers:
            result.append(hdlr)
        return result
    def removeAllHandlers(self):
        count = 0
        for hdlr in self.getHandlerList():
            result = self.loggingLogger.removeHandler(hdlr)
            count = count + 1
        return count
    def getFormatterDict(self):
        result = {}
        for hdlr in self.loggingLogger.handlers:
            result[hdlr] = hdlr.formatter
        return result
    def setFormatter(self,formatter):
        for hdlr in self.loggingLogger.handlers:
            hdlr.setFormatter(formatter)
