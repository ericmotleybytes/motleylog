import pprint
from motleylog.motleylogger import MotleyLogger
from motleylog.motleyformatter import MotleyFormatter
from motleylog.motleyfilter import MotleyFilter
log1 = MotleyLogger.getLogger("logger1")
log1.addNewStreamHandler()
log1.debug("Log message %s.",0,exc_info=0)

fmt1 = '%(levelname)s: %(asctime)s: %(message)s %(msecs)03d'
for1 = MotleyFormatter(fmt=fmt1,style="%")
log1.setFormatter(for1)
log1.debug("Log message %s.",1)

fmt2 = '{levelname}: {asctime}: {message} {msecs}'
for2 = MotleyFormatter(fmt=fmt2,style="{")
log1.setFormatter(for2)
log1.debug("Log message %s.",2)

fmt3 = '$levelname: $asctime: $message $msecs'
for3 = MotleyFormatter(fmt=fmt3,style="$")
log1.setFormatter(for3)
log1.debug("Log message %s.",3)

fmt4 = '%(levelname)s: %(asctime)s: %(message)s'
for4 = MotleyFormatter(fmt=fmt4,style="%",precision=9)
log1.setFormatter(for4)
log1.debug("Log message %s.",4)

fmt5 = '%(levelname)-8s: %(asctime)s: %(message)s'
for5 = MotleyFormatter(fmt=fmt5,style="%",precision=3)
log1.setFormatter(for5)
log1.trace("Log message %s.",5)
log1.debug("Log message %s.",5)
log1.info("Log message %s.",5)
#log1.warning("Log message %s.",5)
log1.error("Log message %s.",5)
log1.fatal("Log message %s.",5)
log1.critical("Log message %s.",5)
log1.printCounts()

pp = pprint.PrettyPrinter(width=100, compact=True)
fil1 = MotleyFilter()
fil1.add_exclude_rule("msg","*SKIP*")
pp.pprint(fil1.get_filter_rules())
handlers = log1.getHandlers()
for handler in handlers:
    print("handler.name=" + str(handler.name))
    print("handler.class=" + handler.__class__.__name__)
handlers[0].addFilter(fil1)
log1.debug("SKIP:Do not see this message.")
log1.debug("See this message.")
log1.trace("levelno={levelno} filename={filename} pathname={pathname} funcname={funcname}")
#log1.trace("levelno={levelno} filename={filename} pathname={pathname}")
log1.printCounts()
def subber():
    log1.trace("levelno={levelno} filename={filename} pathname={pathname} funcname={funcname}")

subber()
