from os import listdir, makedirs
from os.path import join, isdir, dirname, abspath, exists
from mutagen.easyid3 import EasyID3
from mutagen.flac import FLAC
import mutagen.id3
from PIL import Image
from mutagen.id3 import ID3, APIC


class List:
    masterList = []
    song_count = 0
    not_count = 0
    albumList = []
    artistList = []
    path = ""

    def setPath(self, path):
        self.path = path

    def add(self, file, path):
        type = file[-4:].replace(".", "")
        if type == "flac" or type == "mp3":
            # print("is song")
            # self.song_count+=1
            song = SongFile(file, path, type)
            self.masterList.append(song)
        else:
            # print("not song")
            # self.not_count+=1
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
        # print(self.song_count)
        # print(self.not_count)

    def makeAlbumList(self):
        for song in self.masterList:
            tup = [self.legalize(song.albumArtist), self.legalize(song.album)]
            if tup not in self.albumList:
                self.albumList.append(tup)
            if tup[0] not in self.artistList:
                self.artistList.append(tup[0])
        self.albumList.sort()
        self.artistList.sort()
        print(self.albumList)
        print(self.artistList)

    def makeFolder(self):
        for artist in self.artistList:
            path2 = self.path + "\\new\\" + artist
            if not exists(path2):
                makedirs(path2)
        for album in self.albumList:
            path3 = self.path + "\\new\\" + album[0] + "\\" + album[1]
            if not exists(path3):
                makedirs(path3)

    def legalize(filename):
        def safe_char(c):
            if c not in ['/', '\\', ':', '*', '?', '<', '>', '|']:
                return c
            else:
                return ""

        return "".join(safe_char(c) for c in filename).rstrip("_")


class SongFile:
    title = "Tagging Error"
    albumArtist = "Tagging Error"
    album = "Tagging Error"
    track = "-1"
    path = "Tagging Error"
    image = None

    def __init__(self, song, path, type):
        self.path = path + "\\" + song
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
            self.album = metaData["album"][0]
        except:
            print("***" + song + "Album Error")
        try:
            self.track = metaData["tracknumber"][0].split('/')[0]
        except:
            print("***" + song + "Track number Error")
        if(type == "flac"):
            with open('image.jpg', 'wb') as img:
                img.write(metaData.pictures[0].data)
                self.image = Image.open('image.jpg')
        else:
            audio = ID3(self.path)
            with open('image.jpg', 'rb') as albumart:
                audio['APIC'] = APIC(
                    encoding=3,
                    mime='image/jpeg',
                    type=3, desc=u'Cover',
                    data=albumart.read()
                )
                self.image = Image.open('image.jpg')






    def printSong(self):
        print("title : " + self.title
              + "; albumArtist : " + self.albumArtist
              + "; album : " + self.album
              + "; track : " + self.track)


def main():
    l = List
    path = input("What is the path to work with? ('q' for the directory of the python file): ")
    if path == 'q':
        path = dirname(abspath(__file__))
    # path = "D:\Music\Kanye West\Graduation"
    l.setPath(l, path)
    l.makeMasterList(l, path)
    # l.printMasterList(l)
    l.makeAlbumList(l)
    l.makeFolder(l)


if __name__ == '__main__':
    main()
