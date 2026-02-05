import mysql.connector
import os

'''
Class for establishing a connection to the database and execute queries on the database
'''

class DBConnection:
    def __init__(self, host: str = None, user: str = None, password: str = None):
        # Use environment variables if parameters are not provided
        if host is None:
            host = os.getenv("DB_HOST", "127.0.0.1")
        if user is None:
            user = os.getenv("DB_USER", "root")
        if password is None:
            password = os.getenv("DB_PASSWORD", "admin")
        self.conn = mysql.connector.connect(
            host=host,
            user=user,
            password=password,
            use_pure=True
        )
        """
        intialize variables
        """
        self.cursor = self.conn.cursor()

    def check_connection(self):
         '''
         Test database connection
         '''
         self.conn.ping(reconnect=True, attempts=1, delay=0)

    def query(self, query: str) -> list:
        '''
        executes a SQL query and returns the result
        '''
        self.cursor.execute(query)
        return self.cursor.fetchall()

if __name__ == "__main__":
        # test database connection
        try:
            db_conn = DBConnection()
            db_conn.check_connection()
            print("Connection Established")

        except mysql.connector.Error as err:
            print(f"Error: {err}")


