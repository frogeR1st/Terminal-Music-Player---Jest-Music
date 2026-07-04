# Classes
from CustomClasses import AlbumInformation, SongInformation, MusicalInformation, Vector

# Packages
import curses
import json
import os

# Variables
# Music
ArtistElements: list[AlbumInformation] = []
AlbumElements: list[AlbumInformation] = []
SongElements: list[SongInformation] = []

AllElements: list = ArtistElements + AlbumElements + SongElements

# Screen
CurrentScreen: str = "loading"

Config: dict = {}
SongData: dict = {}

# Constants
WINDOW_SIZE: Vector = Vector(100, 40)

LOG_PATH: str = "/home/User/.cache/badNam3/"
LOG_FILENAME: str = "Log.txt"

CONFIG_PATH: str = "/home/User/.config/badNam3/"
CONFIG_FILENAME: str = "MusicPlayerConfig.json"
CONFIG_DUMMY_DATA: dict = {"MusicDirectory": "/home/User/Music/test"}

MUSIC_DATA_PATH: str = "/home/User/.cache/badNam3/"
MUSIC_DATA_FILENAME: str = "MusicData.json"
MUSIC_DATA_DUMMY_DATA: dict = {}


# Mini Functions


def CreatePath(path: str) -> bool:
    # Tests directiory and creates directory
    try:
        os.mkdir(path)
        # AddToLog(f"Created Path {path}, returning True")
        return True

    except FileExistsError:
        # AddToLog(f"Path {path} already exists, returning False")
        return False


def CreateFile(file: str):
    f = open(file, "a")
    f.close()
    # AddToLog(f"Attempted to create file {file}, returning True")


def getJSON(file: str) -> dict:
    stringData: str = ""
    dictData: dict = {}

    f = open(file)
    stringData = f.read()
    f.close()

    dictData = json.loads(stringData)

    return dictData


def setJSON(file: str, data: dict = {}) -> str:
    stringData: str = ""

    stringData = json.dumps(data)

    f = open(file, "w")
    f.write(stringData)
    f.close()

    return stringData


# Startup
# Log
LogMessages: list[str] = []
ShowingLog: bool = False


def AddToLog(Message):
    Message = str(Message)

    LogMessages.append(Message)
    Scroll: int = 1

    CreatePath(LOG_PATH)
    CreateFile(LOG_PATH + LOG_FILENAME)

    f = open(LOG_PATH + LOG_FILENAME, "a")
    f.write(Message + "\n")
    f.close()

    if ShowingLog:  # Currently Broken, when there are too many messages, there is an error as you can't draw outside the terminal
        if len(LogMessages) % 5 == 0:
            StdScr.addstr(len(LogMessages) - Scroll, 50, "5th message")
            Scroll = 0

        try:
            StdScr.addstr(len(LogMessages) - Scroll, 0, Message)
            StdScr.refresh()
        except Exception:
            StdScr.addstr(
                len(LogMessages) - Scroll, 0, "Message too long, see log file"
            )
            StdScr.refresh()


def ShowLog():
    StdScr.clear()
    indx: int = 0
    for Message in LogMessages:
        StdScr.addstr(indx, 0, Message)
        indx += 1
    StdScr.refresh()


# Adds new session to log txt file
f = open(LOG_PATH + LOG_FILENAME, "a")
f.write("\n>-----New Session-----<\n\n")
f.close()

# Init
StdScr = curses.initscr()
AddToLog("Initilized Screen")
StdScr.nodelay(True)
AddToLog("nodelay(True) Called")
curses.noecho()
AddToLog("noecho() Called")

# Create Windows
InformWindow = curses.newwin(98, 1, 1, 1)
AddToLog("Inform Window Created | 98x1 @ 1,1")
MainWindow = curses.newwin(98, 32, 3, 1)
AddToLog("Main Window Created | 98x32 @ 1,3")
MusicPlayerWindow = curses.newwin(98, 3, 36, 1)
AddToLog("Music Player Window Created | 98x3 @ 1,36")


# Main Functions
def GetConfig():
    global Config

    # Creating File
    CreateFile(CONFIG_PATH + CONFIG_FILENAME)

    # Checks if file is empty
    f = open(CONFIG_PATH + CONFIG_FILENAME)
    length = len(f.read())
    f.close()
    AddToLog(f"Found file length of Config to be {length}")

    if length <= 0:  # Add dummy data if file is empty
        AddToLog("file length of Config is too small. refilling")
        setJSON(CONFIG_PATH + CONFIG_FILENAME, CONFIG_DUMMY_DATA)
        AddToLog("Added dummy data to config")
        Config = CONFIG_DUMMY_DATA
        AddToLog("Now using dummy data for config, now returning")
        return

    Config = getJSON(CONFIG_PATH + CONFIG_FILENAME)
    AddToLog("read data from config")


def GetMusicData():
    global MusicData

    # Creating File
    CreateFile(MUSIC_DATA_PATH + MUSIC_DATA_FILENAME)

    # Checks if file is empty
    f = open(MUSIC_DATA_PATH + MUSIC_DATA_FILENAME)
    length = len(f.read())
    f.close()
    AddToLog(f"Found file length of Music Data to be {length}")

    if length <= 0:  # Add dummy data
        AddToLog("file length of Music Data is too small. refilling")
        setJSON(MUSIC_DATA_PATH + MUSIC_DATA_FILENAME, MUSIC_DATA_DUMMY_DATA)
        AddToLog("Added dummy data to music data")
        MusicData = MUSIC_DATA_DUMMY_DATA
        AddToLog("Now using dummy data for Music Data, now returning")
        return

    MusicData = MUSIC_DATA_DUMMY_DATA


def _ready():
    CreatePath(MUSIC_DATA_PATH)  # Creates Path
    GetConfig()
    GetMusicData()


def GatherFiles(directory: str) -> dict:
    Files: dict = {}
    Songs: list[str] = []
    SongsFull: list[str] = []
    Directories: list[str] = []
    DirectoriesFull: list[str] = []

    AddToLog(f"Testing Directory: {directory}")

    for file in os.listdir(directory):
        try:
            if file[-4] == ".":
                AddToLog(f"Found Song: {file}")
                Files[file] = "Song"
                Songs.append(file)
                SongsFull.append(f"{directory}/{file}")
            else:
                AddToLog(f"Found Directory: {file}")
                Files[file] = {}
                Directories.append(file)
                DirectoriesFull.append(f"{directory}/{file}")

        except IndexError:
            AddToLog(f"Found Directory: {file} - file too small")
            Files[file] = {}
            Directories.append(file)
            DirectoriesFull.append(f"{directory}/{file}")

    for innerDirectory in Directories:
        AddToLog("> Attempting to go deeper")
        GatheredFiles: dict = GatherFiles(f"{directory}/{innerDirectory}")

        Files[innerDirectory] = GatheredFiles["files"]
        Songs = Songs + GatheredFiles["songs"]
        SongsFull = SongsFull + GatheredFiles["songsFull"]
        Directories = Directories + GatheredFiles["directories"]
        DirectoriesFull = DirectoriesFull + GatheredFiles["directoriesFull"]

    return {
        "files": Files,
        "songs": Songs,
        "directories": Directories,
        "songsFull": SongsFull,
        "directoriesFull": DirectoriesFull,
    }


def GetAlbumElement(Name: str, From: list) -> AlbumInformation:
    AddToLog(f"looking for: {Name}")
    for element in From:
        AddToLog(f"looking at: {element.Name}")
        if element.Name == Name.strip(" "):
            AddToLog(f"found: {element.Name}")
            return element

    raise ModuleNotFoundError


def FilesIntoElements(Directories: list[str], SongDirectories: list[str]):
    Directories = sorted(Directories, key=len)
    SongDirectories = sorted(SongDirectories, key=len)

    AddToLog(f"Dir: {Directories}")
    AddToLog(f"songDir: {SongDirectories}")

    for directory in Directories:
        splitDir: list = directory.replace(Config["MusicDirectory"], "").split("/")
        splitDir.pop(0)

        element = AlbumInformation()
        element.Name = splitDir[-1].strip(" ")
        element.Path = directory

        if len(splitDir) == 1:
            # Artist
            element.Artist = element
            ArtistElements.append(element)
        else:
            # Album
            Art: AlbumInformation = GetAlbumElement(splitDir[0], ArtistElements)
            element.Artist = Art
            AlbumElements.append(element)
            Art.Roster.append(element)

    for songDirectory in SongDirectories:
        splitSongDir: list = songDirectory.replace(Config["MusicDirectory"], "").split(
            "/"
        )
        splitSongDir.pop(0)

        element = SongInformation()
        element.Name = splitSongDir[-1].strip(" ")
        element.Path = songDirectory

        element.Artist = GetAlbumElement(splitSongDir[0], ArtistElements)

        if splitSongDir[-2] == splitSongDir[0]:
            element.Album = element.Artist
        else:
            element.Album = GetAlbumElement(splitSongDir[-2], AlbumElements)
            element.Album.Roster.append(element)

        SongElements.append(element)


def _updateMusicData():
    # Get files from directory
    Files: dict = GatherFiles(Config["MusicDirectory"])
    AddToLog(f"Finished Gathering Files, Tree: {Files}")

    FilesIntoElements(Files["directoriesFull"], Files["songsFull"])
    AddToLog(f"Artists: {ArtistElements}")
    AddToLog(f"Albums: {AlbumElements}")
    AddToLog(f"Songs: {SongElements}")

    # for file in os.listdir(Config["MusicDirectory"]):
    #    if file[-4] == ".":
    #        Files[file] = "Song"
    #    else:
    #        Files[file] = {}

    pass
    # Directories = Artists
    # Dsirectoryies in Directories = Albums/EP's
    # Songs in Directories = Singles
    # Songs in Directories in Directories = Songs
    #
    # Get all artists, albums, songs, from directory
    # Get all artists, arbums, songs, from cache
    #
    # Remove none existant songs from cache
    # Add new songs to cache
    # Remove none existant artists from cache
    # Add new artists to cache
    # Remove none existant albums from cache
    # Add new albums to cache
    #
    # try to add meta date to the songs, albums, artists, so you can rename and move songs


def _ElementHandler():
    pass


def _drawing():
    pass


def _inputHandler():
    pass


# Running Main Funtions

_ready()
_updateMusicData()
_ElementHandler()
_drawing()
_inputHandler()
