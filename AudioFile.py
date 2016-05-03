from vlc import MediaPlayer
from os import walk
from random import choice

audio_dir = "audio"
syllable_seperator = "_"

class AudioFile():
    def __init__(self):
        self.__filename = self.read_file()
        self.__audio = MediaPlayer(audio_dir + "/" + self.__filename)
        self.play()

    def play(self):
        self.__audio.stop()
        self.__audio.play()

    def check_answer(self, answer):
        return answer == self.__filename.split("__")[0].replace("_","")

    def read_file(self):
        _, _, filenames = next(walk(audio_dir))
        return choice(filenames)



