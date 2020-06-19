""" Simple string match globber; support "*" matching in strings. """
import re

def glob_to_re(glob):
    """Translate a shell glob-like pattern to a regular expression.

    Currently there is no way to quote glob metacharacters "*" and "?".

    Parameters:
        glob (str) : A glob like pattern using "*" to match any number of chars and "?" to match a single char.

    Returns:
        str : An equivalent regular expression.
    """
    globOffset = 0
    globLen    = len(glob)
    regex      = '^'
    while globOffset < globLen:
        globChar   = glob[globOffset]
        globOffset = globOffset + 1
        if globChar == "*":
            regex = regex + '.*'
        elif globChar == "?":
            regex = regex + '.'
        elif globChar in [".","[","]","\\","^","$","+","{","}","|","(",")"]:
            regex = regex + '\\' + globChar
        else:
            regex = regex + globChar
    regex = regex + "$"
    return regex

def string_matches_glob(theString,globPattern):
    """Test if a string matchs a glob-pattern.

    Parameters:
        theString (str) : The string to test.
        globPattern (str) : A shell-glob-like matching pattern. "*" matches any number of any character.
            "?" matches any single character. For example: "mypackage.*" or "abc*.?.txt".

    Returns:
        bool : True if the string matches, else False.
    """
    regex = glob_to_re(globPattern)
    match = re.search(regex,theString)
    if match is None:
        result = False
    else:
        result = True
    return result
