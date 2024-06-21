import mysql.connector

class Database:
    def __init__(self):
        self.db_connection = mysql.connector.connect(
            host="127.0.0.1",
            user="root",
            password="Admin@!2345",
            database="fd"
        )
        self.db_cursor = self.db_connection.cursor()

    def execute(self, query, params=None):
        self.db_cursor.execute(query, params)
        self.db_connection.commit()

    def fetchone(self, query, params=None):
        self.db_cursor.execute(query, params)
        return self.db_cursor.fetchone()

    def fetchall(self, query, params=None):
        self.db_cursor.execute(query, params)
        return self.db_cursor.fetchall()
