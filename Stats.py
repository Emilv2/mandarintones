import os.path
import sqlite3
import datetime
import logging
import re

logger = logging.getLogger(__name__)

STATS_DB_FILE = "stats.db"

class Stats():


    def __init__(self):
        if not os.path.isfile(STATS_DB_FILE):
            self._create_stats_db()
        self.__connection = sqlite3.connect(STATS_DB_FILE)
        self.__cursor = self.__connection.cursor()


    def add_stats(self, file_name, answer):
        assert is_valid_file_name(file_name)
        assert is_valid_answer(answer, file_name)
        now = datetime.datetime.now()
        try:
            self.__cursor.execute('''insert into stats(ts, filename, answer)
                values(?, ?, ?)''', (now, file_name, answer))
            self.__connection.commit()
            logger.debug("Added answer ({}, {}, {}) into database".format(now,
                    file_name, answer))
        except:
            logger.exception("Failed to add stats")

    def stats_days(self, frm, to):
        ts = datetime.datetime.now()
#         assert type(frm) is datetime
#         assert type(to) is datetime
        return self.__cursor.execute('''select * from stats where :frm <= :ts
                and :ts <= :to''',
                {"frm": frm, "ts": ts, "to":to})

    def _create_stats_db(self):
        self.__connection = sqlite3.connect(STATS_DB_FILE)
        self.__cursor = self.__connection.cursor()
        self.__cursor.execute('''CREATE TABLE stats(
                ts timestamp, filename text, answer text)''')
        logger.info("created new stats database {}".format(STATS_DB_FILE))


def is_valid_file_name(file_name):
    p = re.compile('([a-z]{1,3}[1-5]){1,4}_.+$')
    if type(file_name) is str and p.match(file_name):
        return True
    else:
        return False

def is_valid_answer(answer, file_name):
    assert is_valid_file_name(file_name)
    count = sum(1 for _ in re.finditer('[1-5]',file_name.split('_')[0]))
    p = re.compile('[1-5]{{{0},{0}}}'.format(count))
    if type(answer) is str and p.match(answer):
        return True
    else:
        return False
