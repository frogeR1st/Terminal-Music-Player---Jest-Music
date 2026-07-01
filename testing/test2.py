import curses
import time

StdScr = curses.initscr()
StdScr.nodelay(True)
curses.noecho()

while True:
    StdScr.clear()

    StdScr.addstr(0, 0, str(StdScr.getch()))

    StdScr.refresh()

    time.sleep(1 / 4)

