import logging
import sys
from motleylog.motleylogger import MotleyLogger
from motleylog.motleyformatter import MotleyFormatter
from motleylog.motleyfilter import MotleyFilter
from motleylog.motleystreamhandler import MotleyStreamHandler
#
# Configure a logger which outputs selectively to both stdout and stderr
#
log1      = MotleyLogger.getLogger("logger1")
loglog    = log1.getLoggingLogger()
formatter = MotleyFormatter(
        fmt='%(levelname)-8s: %(asctime)s: %(message)s',
        datefmt='%Y-%m-%d %H:%M:%S .%f', tzstr='UTC', precision=9)
#handler1  = logging.StreamHandler(sys.stdout)
#handler2  = logging.StreamHandler(sys.stderr)
handler1  = MotleyStreamHandler(sys.stdout)
handler2  = MotleyStreamHandler(sys.stderr)
handler1.setLevel(logging.TRACE)
handler2.setLevel(logging.WARNING)
handler1.setFormatter(formatter)
handler2.setFormatter(formatter)
filter1   = MotleyFilter()
filter1.add_exclude_rule("levelno",[logging.WARNING, logging.ERROR, logging.CRITICAL])
filter2   = MotleyFilter()
handler1.addFilter(filter1)
handler2.addFilter(filter2)
loglog.addHandler(handler1)
loglog.addHandler(handler2)
#
# Try some messages.
#
log1.trace("Message 1.")
log1.debug("Message 2.")
log1.info("Message 3.")
handler1.flush()
log1.warning("Message 4.")
log1.error("Message 5.")
log1.fatal("Message 6.")
handler2.flush()
log1.print_logger_info()
#############################################
logger = MotleyLogger()
logger.print_logger_info()
logger.debug("Message 7")
