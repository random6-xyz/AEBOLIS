import sqlite3

class Database:
    def __init__(self):
        self.cursor = sqlite3.connect('databases/mainDB.db').cursor()

    def execute(self, query):
        self.cursor.execute(query)