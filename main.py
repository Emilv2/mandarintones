#!/usr/bin/python3

import sys
import os
import logging
import logging.config
import yaml
import vlc
from PyQt5.QtWidgets import (QWidget, QPushButton, QApplication, QGridLayout,
        QLabel, QLineEdit, QShortcut)
from PyQt5.QtGui import QPainter, QColor, QFont, QKeySequence
from PyQt5.QtCore import Qt

from AudioFile import AudioFile
from Stats import Stats

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
        answer = self.answerEdit.text()
        if self.audiofile.check_answer(answer):
            self.correct_nb +=1
            self.correct_nbLabel.setText(str(self.correct_nb))
            self.audiofile = AudioFile()
        else:
            self.wrong_nb +=1
            self.wrong_nbLabel.setText(str(self.wrong_nb))
        _stats.add_stats(
            answer,
            self.audiofile.get_pinyin(),
            self.audiofile.get_id(),
        )
        self.answerEdit.clear()

def setup_logging(
    default_path='logging.yaml',
    default_level=logging.INFO,
    env_key='LOG_CFG'
):
    """Setup logging configuration

    """
    path = default_path
    value = os.getenv(env_key, None)
    if value:
        path = value
    if os.path.exists(path):
        with open(path, 'rt') as f:
            config = yaml.safe_load(f.read())
        logging.config.dictConfig(config)
    else:
        logging.basicConfig(level=default_level)

if __name__ == '__main__':
    setup_logging()
    logger = logging.getLogger(__name__)
    logger.info('mandarintones started')
    _stats = Stats()
    app = QApplication(sys.argv)
    window = Window()
    sys.exit(app.exec_())
