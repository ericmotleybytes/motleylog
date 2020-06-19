import logging
import motleylog.motleyglobber as mglob
from motleylog.motleydict import MotleyDict
class MotleyFilter(logging.Filter):
    INCLUDE_RULE = "includes"
    EXCLUDE_RULE = "excludes"
    """ A subclass of logging.Filter which facilitates eazy log message filtering. """
    def __init__(self,loggername=''):
        super().__init__(loggername)
        self.filter_rules = {}
        self.rule_types = {MotleyFilter.INCLUDE_RULE,MotleyFilter.EXCLUDE_RULE}
        self.substitute_flag = True

    #####
    # Rule methods
    #####
    def _add_rule(self, record_attr, globs, rule_type):
        if record_attr not in self.filter_rules:
            self.filter_rules[record_attr] = {}
        if rule_type not in self.filter_rules[record_attr]:
            self.filter_rules[record_attr][rule_type] = []
        if isinstance(globs,str):
            self.filter_rules[record_attr][rule_type].append(globs)
        elif isinstance(globs,int):
            self.filter_rules[record_attr][rule_type].append(str(globs))
        elif hasattr(globs,'__iter__'):
            for glob in globs:
                glob = str(glob)
                self.filter_rules[record_attr][rule_type].append(glob)
        else:
            raise ValueError("Unexpected glob: " + str(globs))

    def add_include_rule(self,record_attr,globs):
        self._add_rule(record_attr, globs, MotleyFilter.INCLUDE_RULE)

    def add_exclude_rule(self,record_attr,globs):
        self._add_rule(record_attr, globs, MotleyFilter.EXCLUDE_RULE)

    def get_filter_rules(self):
        return self.filter_rules

    def clear_filter_rules(self):
        self.filter_rules = {}

    def get_substitute_flag(self):
        return self.substitute_flag

    def set_substitute_flag(self, bool_setting=True):
        self.substitute_flag = bool(bool_setting)

    ##########################
    # overloaded filter method
    ##########################
    def filter(self,record):
        for record_attr in self.filter_rules:
            record_attr_value = str(record.__dict__.get(record_attr,"<missing>"))
            filter_rule = self.filter_rules[record_attr]
            for rule_type in self.filter_rules[record_attr]:
                if rule_type==MotleyFilter.INCLUDE_RULE:
                    includes = self.filter_rules[record_attr][rule_type]
                    subresult = False
                    for glob in includes:
                        glob = str(glob)
                        if mglob.string_matches_glob(record_attr_value,glob):
                            subresult = True
                            break
                    if subresult==False:
                        return 0   # filter
                elif rule_type==MotleyFilter.EXCLUDE_RULE:
                    excludes = self.filter_rules[record_attr][rule_type]
                    subresult = True
                    for glob in excludes:
                        glob = str(glob)
                        if mglob.string_matches_glob(record_attr_value, glob):
                            subresult = False
                            break
                    if subresult == False:
                        return 0  # filter
                else:
                    raise ValueError(rule_type + " is not a valid filter rule type.")
        # If we made it this far we should log message.
        # But first, do possible message placeholder substitution if enabled.
        # For example, if the log message was "Message at level {levelno}." the __dict__["levelno"] attribute of the
        # current log record would replace {levelno}. For a DEBUG log message the message would then be output
        # as "Message at level 10.". If the attribute name is not found then that part of the text remains unchanged.
        if self.get_substitute_flag():
            defaulting_dict = MotleyDict(record.__dict__)
            newmsg = record.msg.format_map(defaulting_dict)
            record.msg = newmsg
        # Return 0 for no logging, 1 for yes logging.
        return 1
