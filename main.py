#!/usr/bin/python3

import sys
import vlc
from PyQt5.QtWidgets import (QWidget, QPushButton, QApplication)

from AudioFile import AudioFile

class Window(QWidget):

    def __init__(self):

        super().__init__()

        self.initUI()
        self.audiofile = AudioFile()

    def initUI(self):
        grid = QGridLayout()
        self.setLayout(grid)

        play = QPushButton('Play', self)
        play.clicked.connect(self.play)

        check = QPushButton('Check', self)
        check.clicked.connect(self.check)

        self.show()

    def play(self):
        self.audiofile.play()

    def check(self):
        self.audiofile.check_answer()


if __name__ == '__main__':

    app = QApplication(sys.argv)
    window = Window()
    sys.exit(app.exec_())
