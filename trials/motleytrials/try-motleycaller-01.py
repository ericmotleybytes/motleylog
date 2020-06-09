from motleylog.motleycaller import MotleyCaller
class Simple:
    def __init__(this):
        pass
    def try1(this):
        caller = MotleyCaller()
        #print(f'module={caller.getCallerModuleName()}')
        #print(f'package={caller.getCallerPackageName()}')
        #print(f'file={caller.getCallerFileName()}')
        #print(f'class={caller.getCallerClassName()}')
        #print(f'function={caller.getCallerFunctionName()}')
        #print(f'lineno={caller.getCallerLine()}')

        return 1
    def try2(this):
        return this.try1() + 1
    @staticmethod
    def try3():
        s3 = Simple()
        return s3.try1() + 1

print("*******************************")
print("**** caller is an instance ****")
print("*******************************")
s = Simple()
s.try2()
print("****************************")
print("**** caller is a static ****")
print("****************************")
Simple.try3()
# try calling from class method
# try calling from lambda
# try calling from callable
