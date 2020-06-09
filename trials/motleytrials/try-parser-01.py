import parser
import symbol
import token
import pprint

def printNestedSymbolList(theEntry,level=0):
    #print(f'level={level}')
    entryTypeName = type(theEntry).__name__
    dotIndent   = "." * (level * 2)
    starIndent  = "=" * (level * 2)
    spaceIndent = " " * ((level+1)*2)
    if entryTypeName!='list':
        msg = f'Entry type ({entryTypeName}) is not a list.'
        raise RuntimeError(msg)
    parseTypeInt = theEntry[0]
    if parseTypeInt in token.tok_name:
        parseTypeStr = "TOK:" + token.tok_name[parseTypeInt]
    elif parseTypeInt in symbol.sym_name:
        parseTypeStr = "SYM:" + symbol.sym_name[parseTypeInt]
    else:
        parseTypeStr = str(parseTypeInt)
    idx = -1
    for parseData in theEntry:
        idx = idx + 1
        if idx==0:
            continue
        parseData    = theEntry[idx]
        if type(parseData).__name__=='list':
            print(f'{dotIndent}{parseTypeStr}=...')
            printNestedSymbolList(parseData,level+1)
        else:
            print(f'{dotIndent}{parseTypeStr}={parseData}')

source1 = "a = 42"
st1 = parser.suite(source1)   # returns an ST object
print(st1)
stlist1 = parser.st2list(st1)
printNestedSymbolList(stlist1)
#for entry in stlist1:
#    print(entry)
#pprint.pprint(symbol.sym_name)
#pprint.pprint(token.tok_name)
