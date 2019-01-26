import scrubber
from os.path import isfile, isdir

LIST_LOCATION = 'list.txt'

def main():
    function = input("What would you like to do? \n"
                     " A. Scrub based on keyword \n"
                     " B. Scrub based on terms.txt \n"
                     " C. Edit terms.txt \n"
                     "Your Choice: ")
    if function.upper() == 'A':
        scrubber.Files(getPath(), getTerm())
    elif function.upper() == 'B':
        if not isfile(LIST_LOCATION):
            file = open(LIST_LOCATION, 'w+')
        scrubber.Files(getPath(), makeList(LIST_LOCATION))
        # print(makeList(LIST_LOCATION))
    elif function.upper() == 'C':
        pass
    else:
        print('INVALID')

def getPath():
    path = input("Enter the path for the folder with files to scrub : ")
    while not isdir(path):
        path = input("That's not a valid path, try again: ")
    return path

def getTerm():
    more = 'y'
    terms = []
    while more.upper() == 'Y':
        term = input("What would you like to scrub from these files?: ")
        more = input("Do you have another term to scrub? (Y/N): ")
        terms.append(term)
    return terms

def makeList(file):
    list = []
    fileObject = open(file, 'r')
    for line in fileObject:
        list.append(line. replace('\n', ''))
    return list

if __name__ == '__main__':
    main()