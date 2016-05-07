"""
AudioFile class and all it's helper functions
"""
from os import walk
from random import choice
from vlc import MediaPlayer
AUDIO_DIR = "audio"

class AudioFile():
    """
    Class for the audiofile.
    Provides all methods to interact with the audio:
    play, check answer, ...
    """
    def __init__(self):
        self.__filename = _read_file()
        self.__audio = MediaPlayer(AUDIO_DIR + "/" + self.__filename)
        self.play()

    def play(self):
        """play the audio of the file"""
        self.__audio.stop()
        self.__audio.play()

    def check_answer(self, answer):
        """
        Check if the provided answer is correct.
        The format should be sound + tone and no seperator between syllables
        ie shang4hai3
        """
        return answer == self.__filename.split("__")[0].replace("_", "")

    def __del__(self):
        self.__audio.release()

def _read_file():
    """
    return a random filename from the audio directory
    """
    _, _, filenames = next(walk(AUDIO_DIR))
    return choice(filenames)

