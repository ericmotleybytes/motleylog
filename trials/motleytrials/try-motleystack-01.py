import inspect
from motleylog.motleystack import MotleyStack
ms = MotleyStack()
#ms.prefixAppend("T1")
#ms.outputVar("a","a"*200)
#ms.outputVar("b","b"*200)

# # test 1

# get current frame within raw code
curFrame = inspect.currentframe()
topPrefix = "dumpCurFrame"
ms.dumpCurFrame(topPrefix,"inspect.currentframe called within raw module code",curFrame)
# get current frame within raw code
#curFrame = inspect.currentframe()
#ms.dumpCurFrame(topPrefix,"inspect.currentframe called within util code",curFrame)

# get the current frame within a module function
def tryModuleFunction():
    topPrefix = "dumpCurFrame"
    curFrame = inspect.currentframe()
    ms.dumpCurFrame(topPrefix, "inspect.currentframe called within module function", curFrame)

# get current frame from within a class in various forms
class TryClass:
    def __init__(self):
        self.ms = MotleyStack()
    @staticmethod
    def tryStaticFunction():
        ms = MotleyStack()
        topPrefix = "dumpCurFrame"
        curFrame = inspect.currentframe()
        ms.dumpCurFrame(topPrefix, "inspect.currentframe called within class static function", curFrame)
    @classmethod
    def tryClassMethod(cls):
        ms = MotleyStack()
        topPrefix = "dumpCurFrame"
        curFrame = inspect.currentframe()
        ms.dumpCurFrame(topPrefix, "inspect.currentframe called within class class function", curFrame)
    def tryInstanceMethod(self):
        topPrefix = "dumpCurFrame"
        curFrame = inspect.currentframe()
        self.ms.dumpCurFrame(topPrefix, "inspect.currentframe called within class instance function", curFrame)
tc = TryClass()

tryModuleFunction()
TryClass.tryStaticFunction()
TryClass.tryClassMethod()
tc.tryInstanceMethod()
