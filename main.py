#!/usr/bin/python3

import sys
import vlc
from PyQt5.QtWidgets import (QWidget, QPushButton, QApplication, QGridLayout,
        QLabel, QLineEdit, QShortcut)
from PyQt5.QtGui import QPainter, QColor, QFont, QKeySequence
from PyQt5.QtCore import Qt

from AudioFile import AudioFile

class Window(QWidget):

    def __init__(self):

        super().__init__()

        self.initUI()
        self.audiofile = AudioFile()

    def initUI(self):
        self.wrong_nb = 0
        self.correct_nb = 0
        grid = QGridLayout()
        play = QPushButton('Play', self)
        check = QPushButton('Check', self)
        self.answerEdit = QLineEdit()
        title = QLabel('answer')
        correctLabel = QLabel('correct: ')
        wrongLabel = QLabel('wrong: ')
        self.wrong_nbLabel = QLabel(str(self.wrong_nb))
        self.correct_nbLabel = QLabel(str(self.correct_nb))

        self.setLayout(grid)

        play.clicked.connect(self.play)
        check.clicked.connect(self.check)
        self.answerEdit.returnPressed.connect(self.check)

        grid.addWidget(correctLabel,0,0)
        grid.addWidget(self.correct_nbLabel,0,1)
        grid.addWidget(wrongLabel,0,2)
        grid.addWidget(self.wrong_nbLabel,0,3)
        grid.addWidget(title,1,1)
        grid.addWidget(self.answerEdit,1,2)
        grid.addWidget(play,2,1)
        grid.addWidget(check,2,2)

        self.shortcut = QShortcut(QKeySequence(Qt.Key_Space), self)
        self.shortcut.activated.connect(self.play)


        self.answerEdit.setFocus()

        print(self.__dict__)
        self.show()

    def play(self):
        self.audiofile.play()

    def check(self):
        if self.audiofile.check_answer(self.answerEdit.text()):
            self.correct_nb +=1
            self.correct_nbLabel.setText(str(self.correct_nb))
            self.audiofile = AudioFile()
        else:
            self.wrong_nb +=1
            self.wrong_nbLabel.setText(str(self.wrong_nb))
        self.answerEdit.clear()


if __name__ == '__main__':

    app = QApplication(sys.argv)
    window = Window()
    sys.exit(app.exec_())
