import inspect
class MotleyCaller:
    def __init__(self, extraFrameSkip = 0):
        doPrint = True
        self.callerPackageName  = ""
        self.callerModuleName   = ""
        self.callerClassName    = ""
        self.callerClassObj     = None    # built in Class class
        self.callerFunctionName = ""
        self.callerFunctionObj  = None    # built in function class
        self.callerFileName     = ""
        self.callerLineNumber   = -1
        self.callerFrameInfoObj = None    # inspect.FrameInfo class
        self.callerFrameObj     = None    # inspect.Frame class
        # supporting data
        curFrameObj     = inspect.currentframe()
        outerStackList  = inspect.getouterframes(curFrameObj, 50)  # returns list of inspect.FrameInfo objects
        outerStackLen   = len(outerStackList)
        frameInfoObjIdx = (outerStackLen-1) - (1+extraFrameSkip)
        if frameInfoObjIdx<0 or frameInfoObjIdx>=outerStackLen:
            raise RuntimeError(f'Bad frame index {frameInfoObjIdx} for stack of length {outerStackLen}.')
        frameInfoObj    = outerStackList[frameInfoObjIdx]
        frameObj        = frameInfoObj.frame
        # primary data
        packageName   = frameObj.f_globals['__package__']
        moduleName    = frameObj.f_globals['__name__']
        className     = ""
        classObj      = None
        functionObj   = None
        functionName  = frameInfoObj.function     # a str
        fileName      = frameInfoObj.filename
        lineNumber    = frameInfoObj.lineno
        # more
        codeObj           = frameInfoObj.frame.f_code
        codeSourceLines   = inspect.getsourcelines(codeObj)   # source code as a list of lines
        codeSource        = inspect.getsource(codeObj)        # source code as one string
        frameSourceLines  = inspect.getsourcelines(frameObj)  # source code as a list of lines
        frameSource       = inspect.getsource(frameObj)       # source code as one string
        codeContext       = frameInfoObj.code_context         # some selected lines of caller source code
        codeContextIndex  = frameInfoObj.index                # index of code_context where call actually made
        callingSourceLine = codeContext[codeContextIndex]     # single source line which called (no continuation)
        frameLocals       = frameObj.f_locals                 # dict of local symbol names
        codeArgs          = inspect.getargs(codeObj)
        frameArgValues    = inspect.getargvalues(frameObj)
        if doPrint:
            print(f'module={moduleName}')
            print(f'package={packageName}')
            print(f'class={className}:{str(classObj)}')
            print(f'function={functionName}:{str(functionObj)}')
            print(f'file={fileName}')
            print(f'lineno={lineNumber}')
            print('..........')
            print(f'frameSourceLines={frameSourceLines}')
            #print(f'frameSource={frameSource}')
            print(f'codeSourceLines={frameSourceLines}')
            #print(f'codeSource={codeSource}')
            print(f'codeContext={codeContext}')
            print(f'codeContextIndex={codeContextIndex}')
            print(f'callingSourceLine={callingSourceLine}')
            print(f'frameLocals={frameLocals}')
            print(f'codeArgs={codeArgs}')
            print(f'frameArgValues={frameArgValues}')
            if 'this' in frameLocals.keys():
                temp = frameLocals['this']
                print(f'temp.__class__={temp.__class__.__name__}')
                print(f'isclass={inspect.isclass(temp)}')
                print(f'ismodule={inspect.ismodule(temp)}')
                print(f'isfunction={inspect.isfunction(temp)}')
                print(f'ismethod={inspect.ismethod(temp)}')
                print(f'isroutine={inspect.isroutine(temp)}')
                print(f'iscode={inspect.iscode(temp)}')
                if inspect.isclass(frameLocals['this']):
                    print("this is a class")
                else:
                    print("this is not a class")
            print('')
            # punt? module dict?

        # set instance variables
        self.callerPackageName = packageName
        self.callerModuleName  = moduleName
        self.callerClassName   = className
        self.callerClass       = classObj
        self.functionName      = functionName
        self.functionObj       = functionObj
        self.callerFileName    = fileName
        self.callerLineNumber  = lineNumber
        self.callerFrameInfo   = frameInfoObj
        self.frame             = frameObj
        #
        #print("+"*100)
        #print(f'codemodule={inspect.getmodule(theCode)}')      # module object
        #print(f'code.co_name={theCode.co_name}')               # function name
        #print(f'code.co_names={theCode.co_names}')             # variables inside the function
        #print(f'code.firstlineno={theCode.co_firstlineno}')    # line number where function def begins
        #print(f'code.freevars={theCode.co_freevars}')          # variables used but not defined in function/block
        #print(f'code.varnames={theCode.co_varnames}')          # variables defined inside block
        #sourcelines = inspect.getsourcelines(theCode)
        #idx = -1
        #for sourceline in sourcelines:
        #    idx = idx + 1
        #    print(f' {idx}: {sourceline}')
        ##self.callerLine = theCode.co_firstlineno
        #self.callerLine = frameInfo.lineno
        #self.callerFunctionName = frameInfo.function
        #print(self.frame)
        #print(self.frame.f_locals)
        #print(self.frame.f_globals)
        #print(theCode)
        #print("-"*100)

    def getCallerModuleName(self):
        return self.callerModuleName
    def getCallerPackageName(self):
        return self.callerPackageName
    def getCallerClass(self):
        return self.callerClass
    def getCallerClassName(self):
        return self.callerClassName
    def getCallerFileName(self):
        return self.callerFileName
    def getCallerFrameInfo(self):
        return self.callerFrameInfo
    def getCallerFrame(self):
        return self.callerFrame
    def getCallerFunctionName(self):
        return self.callerFunctionName
    def getCallerLineNumber(self):
        return self.callerLineNumber
