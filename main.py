#!/usr/bin/python3

import sys
import vlc
from PyQt5.QtWidgets import (QWidget, QPushButton, QApplication)

class Window(QWidget):

    def __init__(self):

        super().__init__()

        self.initUI()
        self.p = vlc.MediaPlayer("1-2.mp3")

    def initUI(self):
        play = QPushButton('Play', self)
        play.clicked.connect(self.play)

        self.show()

    def play(self):
        self.p.play()


if __name__ == '__main__':

    app = QApplication(sys.argv)
    window = Window()
    sys.exit(app.exec_())
