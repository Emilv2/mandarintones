#!/usr/bin/python3

import sys
import vlc
from PyQt5.QtWidgets import (QWidget, QPushButton, QApplication, QGridLayout,
        QLabel, QLineEdit)

from AudioFile import AudioFile

class Window(QWidget):

    def __init__(self):

        super().__init__()

        self.initUI()
        self.audiofile = AudioFile()

    def initUI(self):
        grid = QGridLayout()
        play = QPushButton('Play', self)
        check = QPushButton('Check', self)
        self.answerEdit = QLineEdit()
        title = QLabel('answer')

        self.setLayout(grid)

        play.clicked.connect(self.play)
        check.clicked.connect(self.check)
        self.answerEdit.returnPressed.connect(self.check)

        grid.addWidget(title,0,1)
        grid.addWidget(self.answerEdit,0,2)
        grid.addWidget(play,1,1)
        grid.addWidget(check,1,2)

        self.answerEdit.setFocus()

        print(self.__dict__)
        self.show()

    def play(self):
        self.audiofile.play()

    def check(self):
        self.audiofile.check_answer(self.answerEdit.text())
        self.answerEdit.clear()


if __name__ == '__main__':

    app = QApplication(sys.argv)
    window = Window()
    sys.exit(app.exec_())
