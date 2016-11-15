#!/usr/bin/python3

import sys
import os
import logging
import logging.config
import yaml
from AudioFile import AudioFile
from Stats import Stats
import PyQt5.QtWidgets  # import QApplication, QMainWindow
import PyQt5.QtCore  # import QUrl
import PyQt5.QtQuick  # import QQuickView
import PyQt5.QtQml


class QtScoreInterface(PyQt5.QtCore.QObject):

    @PyQt5.QtCore.pyqtSlot()
    def test(self):
        return 5




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
    qApplication = PyQt5.QtWidgets.QApplication(sys.argv)
    window = PyQt5.QtQml.QQmlApplicationEngine("./main.qml")
    # window.setSource(PyQt5.QtCore.QUrl("./main.qml"))
    # window.show()

    qcontext = window.rootContext()
    interface = QtScoreInterface()
    qcontext.setContextProperty("qScoreInterface", interface)

    # interface.signaller_score_a.connect(window.rootObject().updateScoreA)
    # interface.signaller_score_b.connect(window.rootObject().updateScoreB)

    sys.exit(qApplication.exec_())
