import sys

def findEnd(data, openDelim):
    if openDelim not in ['{', '[']:
        raise Exception("Unknown first character")
    if data[0] not in ['{', '[']:
        raise Exception("Unknown first character")
    closeDelim = ''
    if openDelim == '[':
        closeDelim = ']'
    if openDelim == '{':
        closeDelim = '}'
    
    numOpen = 0
    for idx, i in enumerate(data):
        if i == openDelim:
            numOpen = numOpen + 1
        elif i == closeDelim:
            numOpen = numOpen - 1
        if (numOpen == 0):
            return idx
    raise Exception("Could not find close delim")



def parsePrimitive(data):
    data = data.strip()
    if data.startswith('"') and data.endswith('"'):
        return data[1:-1]
    elif len(data) == 1 and data.isalpha():
        return data       
    elif data == 'null':
        return None
    elif data == 'true':
        return True
    elif data == 'false':
        return False
    elif data.isdigit():
        return int(data)
    else:
        raise Exception("Invalid data type")
    
    
def parseObject(data):
    data = data.strip()
    if not (data.startswith('{') and data.endswith('}')):
        raise Exception("The input data does not begin and end with curly brackets")
    data = data[1:-1].strip()
    returnDict = {}
    while data:
        #Find key
        data = data.strip()
        if data and data[0] == ',':
            data = data[1:].strip()
        if data[0] != '"':
            raise Exception("Key not beginning with quote")
        secondQuote = data[1:].find('"')
        if secondQuote == -1:
            raise Exception("Key not ending with quote")
        thisKey = data[1:secondQuote+1]
        # Next thing should be colon
        _, value = data.split(':',1)
        value = value.strip()
        if value[0] == '{':
            valueEnd = findEnd(value, '{')
            thisValue = parseObject(value[:valueEnd+1])
            data = value[valueEnd+1:]
            

        elif value[0] == '[':
            AssertionError("Unimplemented")
            valueEnd = findEnd(value, ']')
            thisValue = parseArray(value)
            # xxx reduce data       
            
        else:
            endValueIndex = value.find(',')
            if endValueIndex == -1:
                thisValue = parsePrimitive(value)
                data = []
            else:
                thisValue = parsePrimitive(value[:endValueIndex])
                data = value[endValueIndex+1:]
                
        returnDict[thisKey] = thisValue    
        
    

    return returnDict


def parseArray(data): 
    returnList = []
    data = data.strip()
    if data and data[0] == ',':
        data = data[1,:]
    if not (data.startswith('[') and data.endswith(']')):
        raise Exception("The input data does not begin and end with square brackets")
    data = data[1:-1]
    
    
    start_open_bracket = data.find('[')       
    if (start_open_bracket != -1):
        beforeBracket = data[:start_open_bracket]
        if (',' in beforeBracket):            
            for item in beforeBracket.split(','):
                if item:
                    returnList.append(parsePrimitive(item))
    else:
        elems = data.split(',')
        for item in elems:
            returnList.append(parsePrimitive(item))
    start_close_bracket = -1    
    if (start_open_bracket != -1):
        start_close_bracket = data.find(']')
        if (start_close_bracket == -1):
            raise Exception("Mismatched square brackets")
        nestedArray = data[start_open_bracket:start_close_bracket+1]
        returnList.append(parseArray(nestedArray))

    if start_close_bracket != -1:
        afterBracket = data[start_close_bracket+1:]
        if (',' in afterBracket):
            for item in afterBracket.split(','):
                if item:
                    returnList.append(parsePrimitive(item))
    return returnList


def parseJSON(inputFile):

    with open(inputFile, 'r') as file:
        data = file.read()    

    return parseObject(data)

def main():
    if len(sys.argv) != 2:
        print("Usage: python JSONParser.py <input_file>")
        sys.exit(1)

    inputFile = sys.argv[1]
    try:
        output = parseJSON(inputFile)
        print(output)
    except Exception as e:
        print(e)
        sys.exit(1)

if __name__ == '__main__':
    main()

