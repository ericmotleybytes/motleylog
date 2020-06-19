import sys
import logging
from motleylog.motleyformatter import MotleyFormatter
from motleylog.motleylogconfig import MotleyLogConfig
from motleylog.motleystreamhandler import MotleyStreamHandler
from motleylog.motleyfilter import MotleyFilter
class MotleyLogger(object):
    motleyLoggers        = {}           # All MotleyLogger instances stored in this dict.
    DEFAULT_LOGGER_NAME  = "MOTLEYLOG"  # Default name for logger.
    COUNTS_DICT_NAME     = "MOTLEYCOUNTS"  # __dict__ entry of a dict with log message counts.

    def _trace_for_logging_logger(self, message, *args, **kws):
        self.log(MotleyLogger.TRACE_LEVEL_NUM, message, *args, **kws)

    def __init__(self, loggerName=None):
        # Do initializations of new instance in __new__ not here in __init__!
        # __init__ might not always get called for this class.
        pass

    def __new__(cls, loggerName=None):
        # Provide a default logger name if not explicitly specified.
        if loggerName is None:
            loggerName = MotleyLogger.DEFAULT_LOGGER_NAME
        else:
            loggerName = str(loggerName)   # Make sure name is a string.
        # Do general logging module configuration ig needed.
        if logging.getLevelName(MotleyLogConfig.TRACE_LEVEL_NUM)!=MotleyLogConfig.TRACE_LEVEL_NAME:
            logging.addLevelName(MotleyLogConfig.TRACE_LEVEL_NUM, MotleyLogConfig.TRACE_LEVEL_NAME)
            logging.__dict__[MotleyLogConfig.TRACE_LEVEL_NAME] = MotleyLogConfig.TRACE_LEVEL_NUM
        # retieve or create new instance
        if loggerName in MotleyLogger.motleyLoggers:
            instance = MotleyLogger.motleyLoggers[loggerName]  # get saved instance
        else:
            instance = object.__new__(cls)
            instance.motleyLoggerName = loggerName
            if loggerName in logging.Logger.manager.loggerDict:
                # logging.Logger already exists, no need to initialize
                instance.loggingLogger = logging.getLogger(loggerName)
                #instance.loggingLogger.trace = MotleyLogger._trace_for_logging_logger
                # Dynamically add trace extension method to logger instance.
                setattr(instance.loggingLogger,
                        MotleyLogConfig.TRACE_METHOD_NAME,
                        MotleyLogger._trace_for_logging_logger)
            else:
                # logging.Logger is new, initialize
                instance.loggingLogger = logging.getLogger(loggerName)
                instance.loggingLogger.setLevel(MotleyLogConfig.TRACE_LEVEL_NUM)
                #formatter = MotleyFormatter()
                #consoleHandler = logging.StreamHandler(sys.stdout)
                #consoleHandler.setFormatter(formatter)
                #consoleHandler.setLevel(logging.DEBUG)
                #instance.loggingLogger.addHandler(consoleHandler)
            # Initialize message counts dictionary.
            instance.__dict__[MotleyLogger.COUNTS_DICT_NAME] = {}
            # Save MotleyLogger instance in motley master dictionary.
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
        elif name in MotleyLogger.motleyLoggers:
            motleyLogger  =  MotleyLogger.motleyLoggers[name]
            loggingLogger = motleyLogger.getLoggingLogger()
            MotleyLogger.motleyLoggers.pop(name)

    def addNewStreamHandler(self,stream=sys.stdout,level=None,formatter=None):
        if level is None:
            level = self.getEffectiveLevel()
        if formatter is None:
            formatter = MotleyFormatter()
        streamHandler = MotleyStreamHandler(stream)
        streamHandler.setFormatter(formatter)
        streamHandler.setLevel(level)
        self.addHandler(streamHandler)
        return streamHandler

    def addNewFileHandler(self,filename,mode='a',encoding='utf-8',level=None,formatter=None,):
        if level is None:
            level = self.getEffectiveLevel()
        if formatter is None:
            formatter = MotleyFormatter()
        fileHandler = logging.FileHandler(filename,mode,encoding)
        fileHandler.setFormatter(formatter)
        fileHandler.setLevel(level)
        self.addHandler(fileHandler)
        return fileHandler

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
    def addFilter(self, filter):
        #for handler in self.getHandlers():
        #    handler.addFilter(filter)
        self.getLoggingLogger().addFilter(filter)
    def callHandlers(self, record):
        return self.loggingLogger.callHandlers(record)
    def critical(self,msg, *args, **kwargs):
        if not self.hasHandlers():
            self.configureBasic()
        kwargs["stacklevel"] = 2
        self.loggingLogger.critical(msg, *args, **kwargs)
        self._trackLog(logging.CRITICAL)
    def debug(self, msg, *args, **kwargs):
        if not self.hasHandlers():
            self.configureBasic()
        kwargs["stacklevel"] = 2
        self.loggingLogger.debug(msg, *args, **kwargs)
        self._trackLog(logging.DEBUG)
    def error(self, msg, *args, **kwargs):
        if not self.hasHandlers():
            self.configureBasic()
        kwargs["stacklevel"] = 2
        self.loggingLogger.error(msg, *args, **kwargs)
        self._trackLog(logging.ERROR)
    def exception(self, msg, *args, exc_info=True, **kwargs):
        if not self.hasHandlers():
            self.addNewStreamHandler()
        kwargs["stacklevel"] = 2
        self.loggingLogger.error(msg, *args, exc_info=exc_info, **kwargs)
    def fatal(self, msg, *args, **kwargs):
        if not self.hasHandlers():
            self.configureBasic()
        kwargs["stacklevel"] = 2
        self.loggingLogger.fatal(msg, *args, **kwargs)
        self._trackLog(logging.FATAL)
    def findCaller(self, stack_info=False, stacklevel=2):
        return self.loggingLogger.findCaller(stack_info=stack_info, stacklevel=stacklevel)
    def getChild(self,suffix):
        return self.loggingLogger.getChild(suffix)
    def getEffectiveLevel(self):
        return self.loggingLogger.getEffectiveLevel()
    def handle(self, record):
        if not self.hasHandlers():
            self.configureBasic()
        return self.loggingLogger.handle(record)
    def hasHandlers(self):
        return self.loggingLogger.hasHandlers()
    def info(self, msg, *args, **kwargs):
        if not self.hasHandlers():
            self.configureBasic()
        kwargs["stacklevel"] = 2
        self.loggingLogger.info(msg, *args, **kwargs)
        self._trackLog(logging.INFO)
    def isEnabledFor(self, level):
        return self.loggingLogger.isEnabledFor(level)
    def log(self, level, msg, *args, **kwargs):
        if not self.hasHandlers():
            self.configureBasic()
        kwargs["stacklevel"] = 2
        self.loggingLogger.log(level, msg, *args, **kwargs)
        self._trackLog(level)
    def makeRecord(self, name, level, fn, lno, msg, args, exc_info, func=None, extra=None, sinfo=None):
        return self.loggingLogger.makeRecord(name,level,fn,lno,msg,args,exc_info,func=func,extra=extra,sinfo=sinfo)
    def removeHandler(self, hdlr):
        return self.loggingLogger.removeHandler(hdlr)
    def setLevel(self, level, all=False):
        if all:
            for hdlr in self.loggingLogger.handlers:
                hdlr.setLevel(level)
        return self.loggingLogger.setLevel(level)
    def warning(self, msg, *args, **kwargs):
        if not self.hasHandlers():
            self.configureBasic()
        kwargs["stacklevel"] = 2
        self.loggingLogger.warning(msg, *args, **kwargs)
        self._trackLog(logging.WARNING)
    def addFilter(self, filter):
        return self.loggingLogger.addFilter(filter)
    def filter(self, record):
        return self.loggingLogger.filter(record)
    def removeFilter(self, filter):
        return self.loggingLogger.removeFilter(filter)

    # more extensions
    def trace(self, msg, *args, **kwargs):
        if not self.hasHandlers():
            self.configureBasic()
        kwargs["stacklevel"] = 2
        self.loggingLogger.log(MotleyLogConfig.TRACE_LEVEL_NUM, msg, *args, **kwargs)
        self._trackLog(MotleyLogConfig.TRACE_LEVEL_NUM)
    def getHandlers(self):
        result = []
        for hdlr in self.loggingLogger.handlers:
            result.append(hdlr)
        return result
    def removeAllHandlers(self):
        count = 0
        for hdlr in self.getHandlers():
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

    def getCounts(self):
        result = {}
        counts = self.__dict__[self.COUNTS_DICT_NAME]
        levels = list(counts.keys())
        levels.append(MotleyLogConfig.TRACE_LEVEL_NUM)
        levels.append(logging.DEBUG)
        levels.append(logging.INFO)
        levels.append(logging.WARNING)
        levels.append(logging.ERROR)
        levels.append(logging.FATAL)
        levels = sorted(set(levels))
        for lvl in levels:
            lvlCount = counts.get(lvl,0)
            result[lvl] = lvlCount
        return result

    def printCounts(self):
        counts = self.getCounts()
        for lvl in counts:
            lvlName  = logging.getLevelName(lvl)
            lvlCount = counts[lvl]
            print(f'{lvlName}: {lvlCount}')

    def print_logger_info(self):
        loglog = self.getLoggingLogger()
        loglogName = loglog.name
        print("MotleyLogger:")
        print("  Name=",loglogName)
        print("  log-repr=",repr(loglog))
        loglogEffLvl  = loglog.getEffectiveLevel()
        loglogEffName = logging.getLevelName(loglogEffLvl)
        print("  EffectiveLevel=",loglogEffLvl,loglogEffName)

        print("  Filters:")
        for filt in loglog.filters:
            loglog.filters.copy()
            print("    filt-repr=",repr(filt))
        print("  Handlers:")
        for hdlr in loglog.handlers:
            print("    hdlt-repr=",repr(hdlr))
            print("      formatter=",repr(hdlr.formatter))
            print("      Filters:")
            for filt in hdlr.filters:
                print("        filt-repr=",repr(filt))

    def reset_logger(self):
        loglog = self.getLoggingLogger()
        loglogFilters = loglog.filters.copy()
        for filt in loglogFilters:
            loglog.removeFilter(filt)
        loglogHandlers = loglog.handlers.copy()
        for hdlr in loglogHandlers:
            hdlr.formatter = None
            loglogHandlerFilters = hdlr.filters.copy()
            for filt in loglogHandlerFilters:
                hdlr.removeFilter(filt)
            loglog.removeHandler(hdlr)

    def configureBasic(self):
        self.reset_logger()
        loglog = self.getLoggingLogger()
        formatter = MotleyFormatter(
                fmt='%(levelname)-8s: %(asctime)s: %(message)s',
                datefmt='%Y-%m-%d %H:%M:%S .%f', tzstr='UTC', precision=9)
        handler1 = MotleyStreamHandler(sys.stdout)
        handler1.setLevel(logging.TRACE)
        handler1.setFormatter(formatter)
        filter1 = MotleyFilter()
        handler1.addFilter(filter1)
        loglog.addHandler(handler1)

    # internal pseudo-private methods
    def _trackLog(self,level):
        counts = self.__dict__[self.COUNTS_DICT_NAME]
        if level not in counts:
            counts[level] = 1
        else:
            counts[level] = counts[level] + 1
