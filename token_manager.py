import sqlite3
import os
import secrets

class TokenManager:
    def __init__(self, db_file):
        self.db_file = db_file
        self.create_table()

    def create_table(self):
        db_dir = os.path.dirname(self.db_file)
        if not os.path.exists(db_dir):
            os.makedirs(db_dir)

        conn = sqlite3.connect(self.db_file)
        c = conn.cursor()
        c.execute('''CREATE TABLE IF NOT EXISTS tokens
                     (token TEXT PRIMARY KEY, user_id INTEGER)''')
        conn.commit()
        conn.close()

    def generate_token(self, user_id):
        token = secrets.token_hex(32)
        conn = sqlite3.connect(self.db_file)
        c = conn.cursor()
        c.execute("INSERT INTO tokens VALUES (?, ?)", (token, user_id))
        conn.commit()
        conn.close()
        return token

    def verify_token(self, token):
        conn = sqlite3.connect(self.db_file)
        c = conn.cursor()
        c.execute("SELECT user_id FROM tokens WHERE token=?", (token,))
        result = c.fetchone()
        conn.close()
        return result[0] if result else None

if __name__ == '__main__':
    from settings import TOKEN_DB
    num_tokens = int(input("Enter the number of tokens to generate: "))
    prefix = input("Prefix String to Add: ")

    token_manager = TokenManager(TOKEN_DB)

    token_folder = 'token_folder'
    if not os.path.exists(token_folder):
        os.makedirs(token_folder)

    for i in range(num_tokens):
        token = prefix + token_manager.generate_token(i + 1)
        with open(os.path.join(token_folder, f'{i + 1}.token'), 'w') as f:
            f.write(token)

    if not os.path.exists('token_db'):
        os.makedirs('token_db')