from motleylog.motleylogger import MotleyLogger
from motleylog.motleyformatter import MotleyFormatter
log1 = MotleyLogger.getLogger("logger1")
log1.debug("Log message %s.",1,exc_info=0)

fmt1 = '%(levelname)s: %(asctime)s: %(message)s %(msecs)03d'
for1 = MotleyFormatter(fmt=fmt1,style="%")
log1.setFormatter(for1)
log1.debug("Log message %s.",2)

fmt2 = '{levelname}: {asctime}: {message} {msecs}'
for2 = MotleyFormatter(fmt=fmt2,style="{")
log1.setFormatter(for2)
log1.debug("Log message %s.",3)

fmt3 = '$levelname: $asctime: $message $msecs'
for3 = MotleyFormatter(fmt=fmt3,style="$")
log1.setFormatter(for3)
log1.debug("Log message %s.",4)

fmt4 = '%(levelname)s: %(asctime)s: %(message)s'
for4 = MotleyFormatter(fmt=fmt4,style="%",precision=9)
log1.setFormatter(for4)
log1.debug("Log message %s.",5)

fmt5 = '%(levelname)s: %(asctime)s: %(message)s'
for5 = MotleyFormatter(fmt=fmt5,style="%",precision=3)
log1.setFormatter(for5)
log1.debug("Log message %s.",5)
