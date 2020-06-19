"""Defines MotleyLogConfig to allow config changes should MotleyLogger conflict with other logging extensions."""
class MotleyLogConfig:
    """Configuration settings which can be changed to resolve potential conflicts with other logging extensions.

    Used by the motleylog.motleylogger.MotleyLogger class when extending the python standard "logging" facility
    to support a new "TRACE" level of messages. Generally these settings do not need to be changed. However, if
    other extensions to "logging" also try to define a new "TRACE" level message there could be conflicts.
    If this happens the "set" methods in this class should be used to change any conflicting settings. These
    changes need to be made before any instances of MotleyLogger are instantiated, however.
    """
    TRACE_LEVEL_NUM   = 8        # The logging level for the new trace messages.
    TRACE_LEVEL_NAME  = "TRACE"  # The name of the new trace level.
    TRACE_METHOD_NAME = "trace"  # The name of the logging method dynamically added to the instantiated logger.

    @classmethod
    def get_trace_level_num(cls):
        """Returns the trace extension logging level number.

        Returns:
            int : The trace extension logging level number.
        """
        return cls.TRACE_LEVEL_NUM

    @classmethod
    def set_trace_level_num(cls,level_num):
        """Sets the trace extension logging level number.

        Parameters:
            level_num (int) : The trace extension logging level number.
        """
        cls.TRACE_LEVEL_NUM = level_num

    @classmethod
    def get_trace_level_name(cls):
        """Returns the trace extension logging level name.

        Returns:
            str : The trace extension logging level name.
        """
        return cls.TRACE_LEVEL_NAME

    @classmethod
    def set_trace_level_name(cls,level_name):
        """Sets the trace extension logging level name.

        Parameters:
            level_name (str) : The trace extension logging level name.
        """
        cls.TRACE_LEVEL_NAME = level_name

    @classmethod
    def get_trace_method_name(cls):
        """Returns the trace extension dynamically added logger method name.

        Returns:
            str : The trace extension dynamically added logger method name.
        """
        return cls.TRACE_METHOD_NAME

    @classmethod
    def set_trace_method_name(cls,method_name):
        """Sets the trace extension dynamically added logger method name.

        Parameters:
            method_name (str) : The trace extension dynamically added logger method name.
        """
        cls.TRACE_METHOD_NAME = method_name
