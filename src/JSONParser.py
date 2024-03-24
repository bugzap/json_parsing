import sys

def parseJSON(inputFile):
    with open(inputFile, 'r') as file:
        data = file.read()
    return data.startswith('{') and data.endswith('}')    

def main():
    inputFile = sys.argv[1]
    if parseJSON(inputFile):
        print('Valid JSON file.');
        print(0)
    else:
        print('Invalid JSON file.')
        print("1")

if __name__ == '__main__':
    main()

