import sqlite3
import os

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DATA_DIR = os.path.join(BASE_DIR, '..', 'data')
DB_PATH = os.path.join(DATA_DIR, 'database.db')

class DatabaseModel :
    def __init__(self):
        self.connection = sqlite3.connect(DB_PATH)
        self.cursor = self.connection.cursor()
        self.cursor.execute("DROP TABLE IF EXISTS DATABASE")
        self.cursor.execute("""
        CREATE TABLE APP (
        IP VARCHAR(255) NOT NULL);
                            """)

    def close_connection(self):
        self.connection.close()
