from os import listdir
from os.path import join, isdir, dirname, abspath
from mutagen.mp3 import MP3
from mutagen.easyid3 import EasyID3
from mutagen.flac import FLAC
import mutagen.id3

class List:
    masterList = []
    song_count = 0
    not_count = 0

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


class SongFile:
    title = "Tagging Error"
    albumArtist = "Tagging Error"
    album = "Tagging Error"
    track = "-1"
    path = "Tagging Error"

    def __init__(self, song, path, type):
        self.path = path + "\\" + song
        if type == "flac":
            metaData = FLAC(self.path)
            try:
                self.title = metaData["title"][0]
            except:
                print("***" + song + "Title Error")
            try:
                self.albumArtist = metaData["albumartist"][0]
            except:
                print("***" + song + "AlbumArtist Error")
                try:
                    self.albumArtist = ''.join(metaData["artists"])
                    print("***" + "But the artist works")
                except:
                    print("*** AND" + song + " Artist Error")
            try:
                self.album = metaData["album"][0]
            except:
                print("***" + song + "Album Error")
            try:
                self.track = metaData["tracknumber"][0].split('/')[0]
            except:
                print("***" + song + "Track number Error")
        elif type == "mp3":
            metaData = MP3(self.path)
            try:
                self.title = ''.join(metaData["TIT2"])
            except:
                print("***" + song + "Title Error")
            try:
                self.albumArtist = ''.join(metaData["TPE2"])
            except:
                print("***" + song + " AlbumArtist Error")
                try:
                    self.albumArtist = ''.join(metaData["TPE1"])
                except:
                    print("***" + song + " Artist Error")
            try:
                self.album = ''.join(metaData["TALB"])
            except:
                print("***" + song + "Album Error")
            try:
                self.track = ''.join(metaData["TRCK"]).split('/')[0]
            except:
                print("***" + song + "Track number Error")

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
    # path = "D:\Music\Childish Gambino"
    l.makeMasterList(l, path)
    l.printMasterList(l)
    # filesAndDirs = listdir()
    # l.fillOutFiles(filesAndDirs)
    # print(filesAndDirs)
    # getFiles()


if __name__ == '__main__':
    main()
