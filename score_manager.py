import sqlite3
import os
import threading

class SQLitePool:
    def __init__(self):
        self._local = threading.local()
        self._initialize_database()

    def _initialize_database(self):
        conn = self.connect()
        c = conn.cursor()

        c.execute('''CREATE TABLE IF NOT EXISTS scores
                        (id INTEGER PRIMARY KEY, user_id INTEGER, score REAL)''')

        conn.commit()
        conn.close()

    def connect(self):
        if not hasattr(self._local, 'conn'):
            if not os.path.exists('score_db'):
                os.makedirs('score_db')
            self._local.conn = sqlite3.connect('score_db/scores.db')
        return self._local.conn

    def close(self):
        if hasattr(self._local, 'conn'):
            self._local.conn.close()
            del self._local.conn

sqlite_pool = SQLitePool()

def add_score(user_id, score):
    conn = sqlite_pool.connect()
    c = conn.cursor()

    c.execute("SELECT MAX(score) FROM scores WHERE user_id=?", (user_id,))
    max_score = c.fetchone()[0]

    if max_score is None or score > max_score:
        c.execute("INSERT INTO scores (user_id, score) VALUES (?, ?)", (user_id, score))
        conn.commit()
        conn.close()
        return f'New score {score} added for user {user_id}'
    else:
        conn.close()
        return f'Score {score} is not higher than the previous highest score {max_score}, not added.'

def get_all_scores():
    conn = sqlite_pool.connect()
    c = conn.cursor()

    c.execute("SELECT user_id, MAX(score) FROM scores GROUP BY user_id ORDER BY MAX(score) DESC")
    all_scores = c.fetchall()

    conn.close()
    return all_scores