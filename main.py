# Classes
from CustomClasses import AlbumInformation, SongInformation, Vector

# Packages
import curses
import json
import os

# Variables
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
CONFIG_DUMMY_DATA: dict = {"FPS": 24, "test": "working"}

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
ShowingLog: bool = True


def AddToLog(Message: str = ""):
    LogMessages.append(Message)

    CreatePath(LOG_PATH)
    CreateFile(LOG_PATH + LOG_FILENAME)

    f = open(LOG_PATH + LOG_FILENAME, "a")
    f.write(Message + "\n")
    f.close()

    if ShowingLog:
        StdScr.addstr(len(LogMessages) - 1, 0, Message)
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


def _ElementHandler():
    pass


def _drawing():
    pass


def _inputHandler():
    pass


# Running Main Funtions


_ready()
_ElementHandler()
_drawing()
_inputHandler()
