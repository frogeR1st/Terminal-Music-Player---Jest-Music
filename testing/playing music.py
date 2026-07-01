from pydub import AudioSegment
from pydub.playback import play

var: str = "/home/User/Music/test/The New Normal/"

sound = AudioSegment.from_mp3(var + "0.mp3")
play(sound)
