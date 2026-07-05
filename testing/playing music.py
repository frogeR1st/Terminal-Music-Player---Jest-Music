from pydub import AudioSegment, playback
import pydub
import simpleaudio
import time


var: str = "/home/User/Music/test/Artist/Single.mp3"

sound = AudioSegment.from_file(var)
print(len(sound[169328:]) / 1000)
sound -= 15

pobj = playback._play_with_simpleaudio(sound[259328:])
pobj.wait_done()

while True:
    print("ehll")
    time.sleep(1 / 24)
