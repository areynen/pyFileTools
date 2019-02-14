from os import listdir, makedirs
from os.path import join, isdir, dirname, abspath, exists

from PIL import Image
from mutagen.easyid3 import EasyID3
from mutagen.flac import FLAC
from mutagen.id3 import ID3, APIC
from shutil import copyfile, move



class List:
    masterList = []
    song_count = 0
    not_count = 0
    albumList = []
    artistList = []
    path = ""
    choice = ""
    toDoNewFolder = ""
    ctr = 0

    def setPath(self, path):
        self.path = path.replace("\\", "/")

    def setSettings(self, c, n):
        self.choice = c
        self.toDoNewFolder = n

    def add(self, file, path):
        type = file[-4:].replace(".", "")
        if type == "flac" or type == "mp3":
            song = SongFile(file, path, type)
            self.masterList.append(song)
        else:
            pass

    def makeMasterList(self, path):
        files = listdir(path)
        for f in files:
            if isdir(join(path, f)):
                self.makeMasterList(self, join(path, f))
            else:
                self.add(self, f, path)

    def printMasterList(self):
        for f in self.masterList:
            f.printSong()

    def makeAlbumList(self):
        for song in self.masterList:
            tup = [self.legalize(song.albumArtist), self.legalize(song.album)]
            if tup not in self.albumList:
                self.albumList.append(tup)
            if tup[0] not in self.artistList:
                self.artistList.append(tup[0])
        self.albumList.sort()
        self.artistList.sort()
        # print(self.albumList)
        # print(self.artistList)

    def makeFolder(self):
        for artist in self.artistList:
            path2 = self.path + "/new/" + artist
            if not exists(path2):
                makedirs(path2)
        for album in self.albumList:
            path3 = self.path + "/new/" + album[0] + "/" + album[1]
            if not exists(path3):
                makedirs(path3)

    def legalize(filename):
        def safe_char(c):
            if c not in ['/', '\\', ':', '*', '?', '<', '>', '|']:
                return c
            else:
                return "_"

        return "".join(safe_char(c) for c in filename).rstrip("")

    def fixSongs(self):
        for song in self.masterList:
            if song.artistChecking():
                song.generateNewTitle()
                song.changeTitle()
                song.changeArtist()
            self.ctr += 1
            print(" %d of %d (%d percent)" %(self.ctr, self.masterList.__len__(), 100*self.ctr/self.masterList.__len__()))

    def moveSongs(self):
        for song in self.masterList:
            source = song.path.replace("\\", "/")
            dest = self.path + "/new/" + self.legalize(song.albumArtist) + "/" + self.legalize(song.album) + "/" + song.fileName
            # destImg = self.path + "/" + "new" + "/" + self.legalize(song.albumArtist) + "/" + self.legalize(song.album) + "/" + "folder.jpg"
            self.moveOrCopy(self, song, dest, source)
            # if not exists(destImg):
            #     song.image.save(destImg)
            self.ctr += 1
            # song.printSong()
            print(" %d of %d (%d percent)" %(self.ctr, self.masterList.__len__(), 100*self.ctr/self.masterList.__len__()))

    def editDirectory(self, s: str):
        if self.toDoNewFolder == 'N':
            return s.replace("/new/", "/")

    def moveOrCopy(self, song, dest, source):
        if self.choice == 1:
            if not exists(dest):
                move(source, dest)
        else:
            if not exists(dest):
                copyfile(source, dest)



class SongFile:

    DEFAULT_TAGGING_NAME = "Tagging Error"

    title = DEFAULT_TAGGING_NAME
    albumArtist = DEFAULT_TAGGING_NAME
    artist = DEFAULT_TAGGING_NAME
    album = DEFAULT_TAGGING_NAME
    track = "-1"
    path = DEFAULT_TAGGING_NAME
    fileName = "Bad File"
    image = None

    def __init__(self, song, path, type):
        self.path = path + "/" + song
        self.fileName = song
        if type == "flac":
            metaData = FLAC(self.path)
        elif type == "mp3":
            metaData = EasyID3(self.path)
        try:
            self.title = metaData["title"][0]
        except:
            print("***" + song + "Title Error")
        try:
            self.albumArtist = metaData["albumartist"][0]
        except:
            print("***" + song + "AlbumArtist Error")
            try:
                self.albumArtist = ''.join(metaData["artist"])
                print("***" + "But the artist works")
            except:
                print("*** AND " + song + " Artist Error")
            try:
                self.albumArtist = ''.join(metaData["artists"])
                print("***" + "But the artist works")
            except:
                print("*** AND " + song + " Artist Error")
        try:
            self.artist = ''.join(metaData["artist"])
        except:
            print("***" + song + "Artist Error")
        try:
            self.album = metaData["album"][0]
        except:
            print("***" + song + "Album Error")
        try:
            self.track = metaData["tracknumber"][0].split('/')[0]
        except:
            print("***" + song + "Track number Error")
        # if type == "flac":
        #     with open('image.jpg', 'wb') as img:
        #         img.write(metaData.pictures[0].data)
        #         self.image = Image.open('image.jpg')
        # elif type == "mp3":
        #     audio = ID3(self.path)
        #     with open('image.jpg', 'rb') as albumart:
        #         audio['APIC'] = APIC(
        #             encoding=3,
        #             mime='image/jpeg',
        #             type=3, desc=u'Cover',
        #             data=albumart.read()
        #         )
        #         self.image = Image.open('image.jpg')

    def printSong(self):
        print("title : " + self.title
              + "; artist : " + self.artist
              + "; albumArtist : " + self.albumArtist
              + "; album : " + self.album
              + "; track : " + self.track)

    def artistChecking(self):
        if self.artist != self.DEFAULT_TAGGING_NAME and self.artist != self.albumArtist:
            return True

    def generateNewTitle(self):
        add = self.artist.replace(self.albumArtist + ', ', '')
        self.title = self.title + ' (feat. ' + add + ')'

    def changeTitle(self):
        try:
            audio = EasyID3(self.path)
        except:
            audio = FLAC(self.path)
        audio['title'] = self.title
        audio.save()

    def changeArtist(self):
        try:
            audio = EasyID3(self.path)
        except:
            audio = FLAC(self.path)
        audio['artist'] = self.albumArtist
        audio.save()


def main():
    l = List
    path = input("What is the path to work with? ('q' for the directory of the python file): ")
    if path == 'q':
        path = dirname(abspath(__file__))
    path = 'D:\Music\Childish Gambino'
    print("Searching " + path)
    l.setPath(l, path)
    l.makeMasterList(l, path)
    l.makeAlbumList(l)

    toDo = input("What do you want to do?\n"
                 + "1. Fix the songs and such\n"
                 + "2. Move around the songs and such\n"
                 + "Choice: ")

    if toDo == '1':
        l.fixSongs(l)

    if toDo == '2':
        choice = input("Which would you rather do?\n"
                     + "1. Move the song to a new folder\n"
                     + "2. Copy the song to a new folder\n"
                     + "Choice: ")
        toDoNewFolder = 'N'
        if choice == '1':
            toDoNewFolder = input("Would you like to make a new folder named 'new' for the songs "
                                  + "(to preserve the old file structure)?: (y/n)")
        l.setSettings(l, choice, toDoNewFolder.upper())
        l.makeFolder(l)
        l.moveSongs(l)


if __name__ == '__main__':
    main()
