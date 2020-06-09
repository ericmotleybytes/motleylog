import os
import inspect
class MotleyStack:
    def __init__(self,theMaxLineLen=None):
        if theMaxLineLen is not None:
            self.maxlinelen = theMaxLineLen
        else:
            #self.maxlinelen = 120
            #self.maxlinelen = 200
            self.maxlinelen = 230
        self.maxlinelen = max(60,self.maxlinelen)
        self.maxlinelen = min(10000,self.maxlinelen)
        self.prefix  = []
        self.indentSize = 0
        self.indentStep = 2
        self.continuationFlag = True
        self.linesep = os.linesep
        self.buffer  = [""]

    def proxyCallerInfo(self):
        """ Determine information about the caller of the caller of this method. """
        callerInfo = {}
        curFrame = inspect.currentframe()
        outerStack = inspect.getouterframes(curFrame, 2)  # c5
        frameIdx = -1
        print("proxyCallerInfo:")
        for frameInfo in outerStack:
            frameIdx = frameIdx + 1
            theFrame   = frameInfo.frame
            thePackage = theFrame.f_globals["__package__"]
            print(f'{frameIdx}: {thePackage}')
        return callerInfo

    def dumpCurFrame(self, topPrefix, curFrameDesc, curFrame=None):
        if curFrame is None:
            framePassedIn = False
            curFrame = inspect.currentframe()
        else:
            framePassedIn = True
        self.formatReset()
        self.prefixAppend(topPrefix)
        self.outputVar("desc", curFrameDesc)
        self.indentRight()
        self.outputVar("curFrame", curFrame)
        self.prefixAppend("curframe")
        self.indentRight()
        # get outer frames
        outerStack = inspect.getouterframes(curFrame, 2)  # c5
        self.outputVar("outerStack", outerStack)  # c6
        self.prefixAppend("outerStack")
        self.indentRight()
        frameIdx = -1
        for frameInfo in outerStack:
            frameIdx = frameIdx + 1
            frameInfoPrefix = "frameInfo" + str(frameIdx)
            self.outputVar(frameInfoPrefix, frameInfo)
            self.indentRight()
            self.prefixAppend(frameInfoPrefix)
            self.outputVar("frame", frameInfo.frame)
            self.outputVar("filename", frameInfo.filename)
            self.outputVar("lineno", frameInfo.lineno)
            self.outputVar("function", frameInfo.function)
            self.outputVar("code_context", frameInfo.code_context)
            self.outputVar("code_context_index", frameInfo.code_context[frameInfo.index])
            self.indentLeft()
            self.prefixPop()
        self.formatReset()
        print("")

    def formatSave(self):
        result = {"prefix":self.prefix, "indent":self.indentSize}
        return result
    def formatRestore(self,savedFormat):
        self.prefix = savedFormat["prefix"]
        self.indentSize = savedFormat["indent"]
    def formatReset(self):
        self.prefix = []
        self.indentSize = 0

    def prefixClear(self):
        self.prefix = []
    def prefixAppend(self,prefixPart):
        self.prefix.append(prefixPart)
    def prefixPop(self):
        if len(self.prefix) > 0:
            self.prefix.pop()
    def prefixStr(self):
        result = ""
        for prefixPart in self.prefix:
            if len(result)==0:
                result = prefixPart.strip()
            else:
                result = result + "." + prefixPart.strip()
        result = "[" + result + "]"
        return result
    def indentStr(self,moreIndent=0):
        result = " " * (self.indentSize+moreIndent)
        return result
    def indentDotStr(self,moreIndent=0):
        result = "." * (self.indentSize+moreIndent)
        return result
    def indentClear(self):
        self.indentSize = 0
    def indentRight(self):
        self.indentSize = self.indentSize + self.indentStep
    def indentLeft(self):
        self.indentSize = max(0,self.indentSize - self.indentStep)

    def setContinuationFlag(self, flag):
        self.continuationFlag = bool(flag)
    def getContinuationFlag(self):
        return self.continuationFlag

    def outputVar(self,varPrefix,theVar):
        summary = {}
        self.prefixAppend(varPrefix)
        theVarCls = "(" + theVar.__class__.__name__ + ")"
        theVarStr = self.prefixStr() + theVarCls + ": " + self.stringClean(theVar)
        buf = [""]
        while theVarStr is not None:
            bufIdx = len(buf) - 1
            if bufIdx==0 and len(buf[bufIdx])==0:
                buf[bufIdx] = self.indentDotStr()
            elif len(buf[bufIdx])==0:
                buf[bufIdx] = self.indentStr(2)
            remainingLen = self.maxlinelen - len(buf[bufIdx])
            if(remainingLen<=0):
                raise RuntimeError("Indent too long.")
            partialStr = theVarStr[0:remainingLen]   # ok if remainingLen longer than string
            buf[bufIdx] = buf[bufIdx] + partialStr
            remainingLen = max(0,len(theVarStr)-remainingLen)
            if remainingLen==0:
                theVarStr = None
            else:
                theVarStr = theVarStr[-remainingLen:]
                if self.continuationFlag:
                    theVarStr = None
                else:
                    buf.append("")    # init continuation line buf
        for bufLine in buf:
            print(bufLine)
        self.prefixPop()

    def stringClean(self,theString):
        result = str(theString).replace("\r","").replace("\n","<eol>")
        return result
