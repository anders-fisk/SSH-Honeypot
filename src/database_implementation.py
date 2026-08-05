import sqlite3
import os

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DATA_DIR = os.path.join(BASE_DIR, '..', 'data')
DB_PATH = os.path.join(DATA_DIR, 'database.db')

class DatabaseModel :
    def __init__(self):
        self.cursor = self.connection.cursor()
        self.cursor.execute("DROP TABLE IF EXISTS DATABASE")
        self.cursor.execute("""
        CREATE TABLE DATABASE (
        IP VARCHAR(255) NOT NULL);
                            """)
        self.connection = sqlite3.connect(DB_PATH)

    def insert_data(self, data):
        self.cursor.execute("INSERT INTO DATABASE VALUES ('{}')".format(data[0]))
        self.connection.commit()
        print("Data Inserted in the table: {}".format(data))

    def show_all_data(self):
        self.cursor.execute("SELECT * FROM DATABASE")
        data_rows = self.cursor.fetchall()
        for row in data_rows:
            print('a')
            print(row)

    def close_connection(self):
        self.connection.close()
