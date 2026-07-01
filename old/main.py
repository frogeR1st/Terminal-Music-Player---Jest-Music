# Scripts
from Basics import SongInfo, Vector

# Packages
import curses
import json
import os
import threading
import time
from pydub import AudioSegment
from pydub.playback import play

# Program
Running: bool = True
Version: str = "0.0"

# Config
configJSON: str = ""
config: dict = {}
configPath: str = "/home/User/.config/badNam3/"
configName: str = "MusicPlayerConfig.json"
configFile: str = configPath + configName

# Screen
StdScr = curses.initscr()
curses.noecho()
StdScr.nodelay(True)

ScrSize: Vector = Vector(100, 40)

# Visual
DebugLog: list[str] = []
VisualQueue: list = []

# Song
CurrentSong: SongInfo = SongInfo(
    Name="Laplace's Angel",
    Artist="Will Wood",
    Album="The New Normal",
    Path="003 Laplace's Angel.mp3",
    StartPosition=0,
    StarRating=5,
)


def checkConfigPath():
    # Tests directiory and creates directory
    try:
        os.mkdir(configPath)
    except FileExistsError:
        pass

    # Tests file and creates file
    try:
        f = open(configFile, "a")
        f.close()

    except FileExistsError:
        pass


def getConfig():
    global configJSON
    global config

    checkConfigPath()

    file = open(configFile)
    configJSON = file.read()
    file.close()

    config = json.loads(configJSON)


def setConfig():
    global configJSON
    global config

    checkConfigPath()

    configJSON = json.dumps(config)

    file = open(configFile, "w")
    file.write(configJSON)
    file.close()


def _ready():
    pass


def InputHandleing():
    # DebugLog.append(str(StdScr.getch()))

    if StdScr.getch() == 32:
        PlaySong("0.mp3")


def _process():
    while Running:
        StdScr.addstr(5, 5, "Be")
        # _visualProcess()
        StdScr.addstr(6, 5, "Af")

        time.sleep(1 / config["FPS"])


def DrawInformation():
    # Draw Line H
    for x in range(0, ScrSize.x - 40, 1):
        StdScr.addstr(2, x, "─")

    # Draw Text
    StdScr.addstr(
        1, 1, f" Jest Sound · Version: {Version} · Options (o)   -   By:BadNam3 "
    )


def DrawQueueBorders():
    # Draw Line H
    for y in range(0, ScrSize.y - 4, 1):
        StdScr.addstr(y, 60, "┃")

    # Draw Line V
    for x in range(ScrSize.x, 60, -1):
        StdScr.addstr(2, x, "━")

    # Add Text
    StdScr.addstr(1, 61, " ·            Play  Queue            · ")


def DrawSongControlBorders():
    # Draw Line
    for x in range(ScrSize.x):
        StdScr.addstr(ScrSize.y - 4, x, "━")

    # Draw Corners
    StdScr.addstr(ScrSize.y - 4, 0, "┣")
    StdScr.addstr(ScrSize.y - 4, ScrSize.x, "┫")


def DrawBorders():
    # Main Borders
    #    Top & Bottom Borders
    for x in range(ScrSize.x):
        StdScr.addstr(0, x, "━")
        StdScr.addstr(ScrSize.y, x, "━")

    #   Left & Right Borders
    for y in range(ScrSize.y):
        StdScr.addstr(y, 0, "┃")
        StdScr.addstr(y, ScrSize.x, "┃")

    #   Corners
    StdScr.addstr(0, 0, "┏")
    StdScr.addstr(ScrSize.y, 0, "┗")
    StdScr.addstr(0, ScrSize.x, "┓")
    StdScr.addstr(ScrSize.y, ScrSize.x, "┛")


def DebugLogHandler(StartPosition: Vector = Vector(0, 0)):
    for log in range(len(DebugLog)):
        StdScr.addstr(StartPosition.y + log, StartPosition.x, DebugLog[log])


def _visualProcess():
    try:
        StdScr.clear()
        DrawInformation()
        DrawQueueBorders()
        DrawBorders()
        DrawSongControlBorders()

        DebugLogHandler()

        StdScr.refresh()
        time.sleep(1 / config["FPS"])

    except Exception:
        StdScr.clear()
        StdScr.addstr(0, 0, "There was an error:")
        StdScr.addstr(1, 0, "Please make the terminal larger")
        StdScr.refresh()


def PlaySong(file: str):
    DebugLog.append(config["MusicPath"] + file)
    sound = AudioSegment.from_mp3(config["MusicPath"] + file)
    play(sound)


#
# DO NOT TOUCH!!!!!!!!
# Calling functions
# DODOO NOT TOUCH IT ALRGHT!!!

getConfig()
_ready()

VisualThread = threading.Thread(target=_visualProcess)
VisualThread.start()

InputThread = threading.Thread(target=InputHandleing)
InputThread.start()

_process()
VisualThread.join()
InputThread.join()
