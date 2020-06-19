""" Defines MotleyDict, a dictionary subclass with gentle defaults for missing keys. """
class MotleyDict(dict):
    """ Defined a dictionary subclass with gentle defaults for missing keys."""
    def __missing__(self, key):
        """This method is called when a key is not found in the dictionary.

        Parameters:
            key (any) : The missing dictionary lookup key.

        Returns:
            str : The key enclosed within { } braces, i.e., "{<missingkey>}".
        """
        return str(key).join("{}")
