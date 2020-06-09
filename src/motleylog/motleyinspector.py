import inspect
class MotleyInspector:
    """Useful program inspections routines."""

    CLASSNAME_KEY    = "class_name"
    FILENAME_KEY     = "filename"
    FRAME_KEY        = "frame"
    FUNCTIONNAME_KEY = "function_name"
    INDEX_KEY        = "index_key"
    LINENO_KEY       = "lineno"
    METHODNAME_KEY   = "method_name"
    MODULENAME_KEY   = "module_name"
    CODECONTEXT_KEY  = "codecontext_key"

    @staticmethod
    def get_caller_info(skip=2):
        """Get information about caller.
           Parameters:
               skip : An integer soecifying how many stack fram levels to skip.
                      skip=1 means "who calls me",
                      skip=2 means "who calls my caller", etc.
        """
        result = {MotleyInspector.MODULENAME_KEY:None,
                  MotleyInspector.CLASSNAME_KEY:None,
                  MotleyInspector.METHODNAME_KEY:None}
        stack = inspect.stack()    # returns stack as a list of FrameInfo's.
        MotleyInspector.print_stack_info(stack)
        start_idx = skip
        #if len(stack) < start_idx + 1:
        if start_idx >= len(stack):
            # no frameinfo for start_idx!
            return result  # nothing else above skip!
        frameinfo_results = MotleyInspector.get_frameinfo_info(stack[start_idx])
        result[MotleyInspector.METHODNAME_KEY] = frameinfo_results[MotleyInspector.FUNCTIONNAME_KEY]
        parent_frame = stack[start_idx][0]
        #print(f'stack[start]={stack[start]}')
        #print(f'stack[start].__class__={stack[start].__class__}')
        module = inspect.getmodule(parent_frame)
        if module is None:
            module_name = "__main__"
        else:
            module_name = module.__name__
        result[MotleyInspector.MODULENAME_KEY] = module_name
        print(f'resultGetCallerInfo=={result}')
        return result

    @staticmethod
    def get_frameinfo_info(frameinfo):
        result = {MotleyInspector.FILENAME_KEY:None,
                  MotleyInspector.LINENO_KEY:None,
                  MotleyInspector.FUNCTIONNAME_KEY:None}
        result[MotleyInspector.FILENAME_KEY]     = frameinfo.filename
        result[MotleyInspector.LINENO_KEY]       = frameinfo.lineno
        result[MotleyInspector.FUNCTIONNAME_KEY] = frameinfo.function
        result[MotleyInspector.FRAME_KEY]        = frameinfo.frame
        result[MotleyInspector.INDEX_KEY]        = frameinfo.index
        result[MotleyInspector.CODECONTEXT_KEY]  = frameinfo.code_context
        #help(frameinfo.function)
        #help(frameinfo.frame)
        print(f"frameinfo_results={result}")
        print(f"frame_f_back={frameinfo.frame.f_back}")
        print(f"frame_f_code={frameinfo.frame.f_code}")
        #help(frameinfo.frame.f_code)
        print(f"frame_f_globals={frameinfo.frame.f_globals}")
        print(f"frame_f_lasti={frameinfo.frame.f_lasti}")
        print(f"frame_f_lineno={frameinfo.frame.f_lineno}")
        print(f"frame_f_locals={frameinfo.frame.f_locals}")
        print(f"frame_f_trace={frameinfo.frame.f_trace}")
        print(f"frame_f_code.co_argcount={frameinfo.frame.f_code.co_argcount}")
        print(f"frame_f_code.co_cellvars={frameinfo.frame.f_code.co_cellvars}")
        print(f"frame_f_code.co_code={frameinfo.frame.f_code.co_code}")
        print(f"frame_f_code.co_consts={frameinfo.frame.f_code.co_consts}")
        print(f"frame_f_code.co_filename={frameinfo.frame.f_code.co_filename}")
        print(f"frame_f_code.co_firstlineno={frameinfo.frame.f_code.co_firstlineno}")
        print(f"frame_f_code.co_flags={frameinfo.frame.f_code.co_flags}")
        print(f"frame_f_code.co_freevars={frameinfo.frame.f_code.co_freevars}")
        print(f"frame_f_code.co_kwonlyargcount={frameinfo.frame.f_code.co_kwonlyargcount}")
        print(f"frame_f_code.co_lnotab={frameinfo.frame.f_code.co_lnotab}")
        print(f"frame_f_code.co_name={frameinfo.frame.f_code.co_name}")
        print(f"frame_f_code.co_names={frameinfo.frame.f_code.co_names}")
        print(f"frame_f_code.co_nlocals={frameinfo.frame.f_code.co_nlocals}")
        print(f"frame_f_code.co_posonlyargcount={frameinfo.frame.f_code.co_posonlyargcount}")
        print(f"frame_f_code.co_stacksize={frameinfo.frame.f_code.co_stacksize}")
        print(f"frame_f_code.co_varnames={frameinfo.frame.f_code.co_varnames}")
        return result

    @staticmethod
    def get_frame_info(frame):
        result = {}
        return result

    @staticmethod
    def print_stack_info(stack):
        level = -1
        for frameinfo in stack:
            level = level + 1
            print(f'stacklevel={level}')
            MotleyInspector.get_frameinfo_info(frameinfo)
