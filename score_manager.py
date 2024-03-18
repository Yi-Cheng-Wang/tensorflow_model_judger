import sqlite3
import os

class ScoreManager:
    def __init__(self, db_file):
        self.db_file = db_file
        self.create_table()

    def create_table(self):
        db_dir = os.path.dirname(self.db_file)
        if not os.path.exists(db_dir):
            os.makedirs(db_dir)

        conn = sqlite3.connect(self.db_file)
        c = conn.cursor()
        c.execute('''CREATE TABLE IF NOT EXISTS scores
                        (id INTEGER PRIMARY KEY, user_id INTEGER, score REAL)''')
        conn.commit()
        conn.close()

    def add_score(self, user_id, score):
        conn = sqlite3.connect(self.db_file)
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

    def get_all_scores(self):
        conn = sqlite3.connect(self.db_file)
        c = conn.cursor()

        c.execute("SELECT user_id, MAX(score) FROM scores GROUP BY user_id ORDER BY MAX(score) DESC")
        all_scores = c.fetchall()

        conn.close()
        return all_scores