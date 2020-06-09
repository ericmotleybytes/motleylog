import inspect
from motleylog.motleystack import MotleyStack
class Class1:
    def __init__(self):
        pass
    def method_1_1(self):
        c2 = Class2()
        c2.method_2_1()

class Class2:
    def __init__(self):
        pass
    def method_2_1(self):
        ms = MotleyStack()
        callerInfo = ms.proxyCallerInfo()
        print(callerInfo)

c1 = Class1()
c1.method_1_1()
