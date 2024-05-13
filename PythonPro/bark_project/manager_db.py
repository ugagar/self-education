from sqlite3 import connect


class DatabaseManager:
    connection = None

    def __init__(self, database_path):
        self.connection = connect(database_path)

    def _execute(self, statement, values=None):
        with self.connection:
            cursor = self.connection.cursor()
            cursor.execute(statement, values or [])
            return cursor

    def __del__(self):
        self.connection.close()
