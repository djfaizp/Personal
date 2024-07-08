import sqlite3

class DatabaseHandler:
    def __init__(self):
        self.conn = sqlite3.connect('attachments.db')
        self.create_table()

    def create_table(self):
        cursor = self.conn.cursor()
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS attachments (
                id INTEGER PRIMARY KEY,
                message_id INTEGER,
                name TEXT,
                size INTEGER,
                mime_type TEXT,
                channel_id INTEGER
            )
        ''')
        self.conn.commit()

    def save_attachment_info(self, file_info):
        cursor = self.conn.cursor()
        cursor.execute('''
            INSERT INTO attachments (message_id, name, size, mime_type, channel_id)
            VALUES (?, ?, ?, ?, ?)
        ''', (file_info['id'], file_info['name'], file_info['size'], file_info['mime_type'], file_info['channel_id']))
        self.conn.commit()

    def close(self):
        self.conn.close()
