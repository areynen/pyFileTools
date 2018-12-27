from os import listdir
from os.path import join, isdir, dirname, abspath


class List:
    masterList = []

    def add(self, file, path):
        s = SongFile(file, path)

    def makeMasterList(self, path):
        files = listdir(path)
        for f in files:
            if isdir(join(path, f)):
                self.makeMasterList(self, join(path, f))
            else:
                self.add(self, f, path)

    def printMasterList(self):
        for f in self.masterList:
            print(f)

    def writeMasterList(self):
        file = open("enumeration.txt", "w")
        for i in range(self.masterList.__len__()-1):
            file.write(self.masterList[i] + "\n")
        try:
            file.write(self.masterList[-1])
        except:
            print("No Song files")


class SongFile:
    title = ""
    albumArtist = ""
    album = ""
    track = -1
    path = ""
    def __init__(self, song, path):
        self.path = path
        self.title = ""
        self.albumArtist = ""
        self.album = ""
        self.track = -1



def main():
    l = List
    path = input("What is the path to enumerate? ('q' for the directory of the python file): ")
    if path == 'q':
        path = dirname(abspath(__file__))
    l.makeMasterList(l, path)
    l.printMasterList(l)
    l.writeMasterList(l)
    # filesAndDirs = listdir()
    # l.fillOutFiles(filesAndDirs)
    # print(filesAndDirs)
    # getFiles()


if __name__ == '__main__':
    main()
