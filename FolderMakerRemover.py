from os.path import isdir, join, exists
from os import listdir, rename, makedirs, rmdir


class Files:
    path = ''
    seasons = 0
    style = 0
    fileList = []
    folderList = []

    def __init__(self, p, s, st, choice):
        if choice:
            self.path = p
            self.seasons = int(s)
            self.style = st
            self.makeFileList(self.path)
            self.arrange()
        if not choice:
            self.path = p
            self.makeFileList(self.path)
            self.unfolder()

    def unfolder(self):
        for f in self.fileList:
            if f.path + '\\' + f.name != self.path + '\\' + f.name:
                rename(f.path + '\\' + f.name, self.path + '\\' + f.name)
                print(f.path + '\\' + f.name + ' -> ' + self.path + '\\' + f.name)
        self.cleanEmptyFolders(self.path)

    def cleanEmptyFolders(self, path):
        while self.folderList.__len__() != 0:
            for f in self.folderList:
                try:
                    rmdir(f.path + "\\" + f.name)
                    self.folderList.remove(f)
                except:
                    pass


    def makeFileList(self, path):
        files = listdir(path)
        for f in files:
            if isdir(join(path, f)):
                self.folderList.append(Folder(f, path))
                self.makeFileList(join(path, f))
            else:
                self.add(f, path)

    def add(self, file, path):
        self.fileList.append(File(file, path))

    def stylize(self, num):
        if num < 10 and self.style == 'A':
            num = '0' + str(num)
        return str(num)

    def arrange(self):
        for file in self.fileList:
            for i in range(self.seasons):
                if 'S' + self.stylize(i+1) in file.name:
                    self.moveFile(file, str(i+1))

    def moveFile(self, file, season):
        path = self.path + "\\" + "Season " + season
        if not exists(path):
            makedirs(path)
        if file.path + "\\" + file.name != path + "\\" + file.name:
            rename(file.path + "\\" + file.name, path + "\\" + file.name)
            print(file.path + "\\" + file.name + " -> " + path + "\\" + file.name)

    def printList(self, list):
        for f in list:
            print(f.getFullPath())


class File:
    name = None
    path = None

    def __init__(self, f, p):
        self.name = f
        self.path = p

    def getFullPath(self):
        return str(self.path + "\\" + self.name)


class Folder:
    name = None
    path = None

    def __init__(self, n, p):
        self.name = n
        self.path = p

    def getFullPath(self):
        return str(self.path + "\\" + self.name)


def main():
    choice = input("What would you like to do?:\n"
                   + "A) Sort by seasons into folder\n"
                   + "B) Unfolder everything\n"
                   + "Choice: ")
    if choice.capitalize() == 'A':
        f = Files(getPath(), getSeasons(), getStyle(), True)
    elif choice.capitalize() == 'B':
        f = Files(getPath(), None, None, False)


def getSeasons():
    s = input("Enter the number of seasons: ")
    while (not s.isdigit()) or int(s) < 1:
        s = input("That's not a valid number, try again: ")
    return s

def getStyle():
    validChoices = ['A', 'B']
    s = input("What kind of style is present?:\n"
                  + "A) S0X\n"
                  + "B) SX\n"
                  + "Choice: ")
    while s.capitalize() not in validChoices:
        s = input("That's not a valid option, try again: ")
    return s.capitalize()

def getPath():
    path = input("Enter the path for the folder to use : ")
    while not isdir(path):
        path = input("That's not a valid path, try again: ")
    return path


if __name__ == '__main__':
    main()
