import os.path
import sqlite3
import datetime
import logging
import re
import AudioFile

logger = logging.getLogger(__name__)

STATS_DB_FILE = "stats.db"

class Stats():


    def __init__(self):
        if not os.path.isfile(STATS_DB_FILE):
            self._create_stats_db()
        self._connection = sqlite3.connect(STATS_DB_FILE)
        self._cursor = self._connection.cursor()
        self._cursor.execute("""PRAGMA foreign_keys = ON""")
        self.add_all_files(AudioFile.AUDIO_DIR)

    def add_stats(self, answer, file_id):
        now = datetime.datetime.now()
        try:
            self._cursor.execute('''
            INSERT INTO stats(answer, ts, file_id)
                values(?, ?, ?)''', (answer, now, file_id))
            self._connection.commit()
            logger.info(
                "Added answer ({}, {}, {}) into database".format(
                    answer, now, file_id)
            )
        except:
            logger.error("Failed to add stats")

    def add_file(self, filename):
        pinyin = filename.split('__')[0]
        file_id = filename.split('__')[1].rsplit('.', 1)[0]
        extension = filename.split('__')[1].rsplit('.', 1)[1]
        try:
            self._cursor.execute('''
            INSERT INTO files(pinyin, file_id, extension)
            VALUES(?, ?, ?)
            ''', (
                pinyin,
                file_id,
                extension))
            logger.debug(
                'new file {} added to database'.format(filename)
            )
        except:
            logger.exception(
                'failed to add {} to database'.format(filename),
                exc_info=True
                )

    def add_all_files(self, directory):
        _, _, filenames = next(os.walk(directory))
        for filename in filenames:
            exists = int(
                self._cursor.execute("""
                SELECT COUNT(1)
                FROM files
                WHERE file_id = ? 
                """, (filename,)).fetchone()[0]
                )
            if exists == 0:
                self.add_file(filename)

    def get_random_file(self):
        file = self._cursor.execute('''
        SELECT *
        FROM files
        WHERE file_id IN (SELECT file_id FROM files ORDER BY RANDOM()) LIMIT 1)
        ''').fetchall()
        return file[0] + "__" + file[1] + ".mp3"

    def timerange(self, frm: datetime, to: datetime) -> list:
        return self._cursor.execute('''
        SELECT *
        FROM stats
        WHERE ts >= ? AND ts < ?
        INNER JOIN files
        ON files.file_id = stats.file_id
        ''', (frm, to)).fetchall()

    def _create_stats_db(self):
        try:
            self._connection = sqlite3.connect(STATS_DB_FILE)
            self._cursor = self._connection.cursor()
            self._cursor.execute("""
            CREATE TABLE files(
            pinyin TEXT NOT NULL,
            file_id TEXT PRIMARY KEY NOT NULL,
            extension TEXT NOT NULL
            )
            """)
            self._cursor.execute("""
            CREATE TABLE stats(
            answer TEXT NOT NULL,
            ts TIMESTAMP NOT NULL,
            file_id TEXT NOT NULL,
            FOREIGN KEY(file_id) REFERENCES files(file_id)
            )
            """)
            self._connection.commit()
            logger.info("created new stats database {}".format(STATS_DB_FILE))
        except:
            logger.error(
                "failed to create new stats database {}".format(STATS_DB_FILE),
                exc_info=True
            )


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
