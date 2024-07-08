import sqlite3

class DatabaseHandler:
    def __init__(self):
        self.conn = sqlite3.connect('bot_database.db')
        self.create_tables()
        self.user_id = None

    def create_tables(self):
        cursor = self.conn.cursor()
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS user_session (
                id INTEGER PRIMARY KEY,
                user_id INTEGER UNIQUE
            )
        ''')
        self.conn.commit()

    def set_user_id(self, user_id):
        cursor = self.conn.cursor()
        cursor.execute('INSERT OR REPLACE INTO user_session (id, user_id) VALUES (1, ?)', (user_id,))
        self.conn.commit()
        self.user_id = user_id

    def get_user_id(self):
        if self.user_id is None:
            cursor = self.conn.cursor()
            cursor.execute('SELECT user_id FROM user_session WHERE id = 1')
            result = cursor.fetchone()
            if result:
                self.user_id = result[0]
        return self.user_id

    def save_attachment_info(self, file_info):
        cursor = self.conn.cursor()
        cursor.execute('''
            INSERT INTO attachments (message_id, name, size, mime_type, channel_id)
            VALUES (?, ?, ?, ?, ?)
        ''', (file_info['id'], file_info['name'], file_info['size'], file_info['mime_type'], file_info['channel_id']))
        self.conn.commit()

    def close(self):
        self.conn.close()
