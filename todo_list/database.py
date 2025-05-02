import pyodbc


class Database:
    def __init__(self):
        self.connection = self.connect()

    def connect(self):
        try:
            return pyodbc.connect(
                'DRIVER={ODBC Driver 17 for SQL Server};'
                'SERVER=localhost;'
                'DATABASE=todo_db;'
                'Trusted_Connection=yes;'
            )
        except Exception as e:
            print(f"Error in database connection: {e}")
            raise Exception(f"Failed to connect to the database: {e}")

    def get_connection(self):
        if not self.connection:
            raise Exception("No active database connection")
        return self.connection

