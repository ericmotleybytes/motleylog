import logging
import sys
TRACE_LEVEL_NUM  = 8
TRACE_LEVEL_NAME = "TRACE"
ln1 = logging.getLevelName(TRACE_LEVEL_NUM)
print(f'ln1={ln1}')
logging.addLevelName(TRACE_LEVEL_NUM,"TRACE")
logging.__dict__[TRACE_LEVEL_NAME] = TRACE_LEVEL_NUM
ln2 = logging.getLevelName(TRACE_LEVEL_NUM)
print(f'ln2={ln2}')
print(logging.__dict__["DEBUG"])
print(logging.__dict__["TRACE"])
def trace(self,message,*args,**kws):
    self.log(TRACE_LEVEL_NUM,message,*args,**kws)
#logging.Logger.trace = trace
logger = logging.getLogger("TRYLOGGER")
#logger.trace = trace
#s = "logger.trace = trace"
#eval(s)
#for k in logger.__dict__:
#    print(k,logger.__dict__[k])
setattr(logger,'trace',trace)
logger.setLevel(logging.TRACE)
formatter = logging.Formatter(
        fmt='%(levelname)s: %(asctime)s: %(message)s', style='%', datefmt='%Y-%m-%d %H:%M:%S %Z%z')
#formatter = logging.Formatter(
#        fmt='%(asctime)s: %(message)s', style='%', datefmt='%Y-%m-%d %H:%M:%S %Z%z')
handler = logging.StreamHandler(sys.stdout)
handler.setFormatter(formatter)
handler.setLevel(logging.TRACE)
logger.addHandler(handler)
logger.debug("message 1")
logger.trace(logger,message="message 2")
for lvl in range(1,101):
    lvlname = logging.getLevelName(lvl)
    if lvlname!= f'Level {lvl}':
        print(lvl,lvlname)
