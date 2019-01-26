from os import listdir, rename
from os.path import join, isdir, splitext


class Files:
    path = ""
    termList = []
    fileList = []

    def __init__(self, p, t):
        self.path = p
        self.termList = t
        self.makeFileList(self.path)
        self.printList()

    def printList(self):
        for f in self.fileList:
            self.fix(f)

    def fix(self, file):
        ctr = 1
        fileName, fileExtension = splitext(file.file)
        fixed = fileName
        if self.termList:
            for term in self.termList:
                fixed = fixed.replace(term, "")
        fixedOG = fixed
        notDone = True
        while notDone:
            while fixed[0] == ' ':
                fixed = fixed[1:]
            while fixed[-1] == ' ' or fixed[-1] == '.':
                fixed = fixed[:-1]
            try:
                rename(file.path + "/" + file.file, file.path + "/" + fixed + fileExtension)
                notDone = False
            except FileExistsError:
                print("Trying fix")
                fixed = fixedOG + " " + str(ctr)
                ctr += 1
        if file.path + "/" + file.file != file.path + "/" + fixed + fileExtension:
            print(file.file + " -> " + fixed.replace(self.path + "/", "") + fileExtension)

    def add(self, file, path):
        self.fileList.append(File(file, path))

    def makeFileList(self, path):
        files = listdir(path)
        for f in files:
            if isdir(join(path, f)):
                self.makeFileList(join(path, f))
            else:
                self.add(f, path)

class File:
    file = None
    path = None

    def __init__(self, f, p):
        self.file = f
        self.path = p
