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
           
            valueEnd = findEnd(value, '[')
            thisValue = parseArray(value[:valueEnd+1])
            data = value[valueEnd+1:]        
            
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
    
    if not (data.startswith('[') and data.endswith(']')):
        raise Exception("The input data does not begin and end with square brackets")
    data = data[1:-1]
    while data:
        data = data.strip()
        if data and data[0] == ',':
            data = data[1:].strip()

        if data[0] == '{':
            valueEnd = findEnd(data, '{')
            thisValue = parseObject(data[:valueEnd+1])
            data = data[valueEnd+1:]
        elif data[0] == '[':
            valueEnd = findEnd(data, '[')
            thisValue = parseArray(data[:valueEnd+1])
            data = data[valueEnd+1:]    
        else:
            endValueIndex = data.find(',')
            if endValueIndex == -1:
                thisValue = parsePrimitive(data)
                data = []
            else:
                thisValue = parsePrimitive(data[:endValueIndex])
                data = data[endValueIndex+1:]

        returnList.append(thisValue)
    
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

