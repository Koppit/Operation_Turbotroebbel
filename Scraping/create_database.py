import mysql.connector
from mysql.connector import Error
import os

HOSTNAME = os.getenv("DB_HOST", "127.0.0.1")
USERNAME = os.getenv("DB_USER", "root")
PASSWORD = os.getenv("DB_PASSWORD", "admin")
FILENAME = "TurbotroebbelSQL.sql"

def execute_sql_file(filename, connection):
    """
    Reads and executes a SQL file
    """
    try:
        cursor = connection.cursor()
        with open(filename, 'r') as file:
            sql_script = file.read()
        # Execute the script with multi=True
        cursor.execute(sql_script, map_results=True)

        print(f"\nSuccessfully executed all statements in {filename}")

    except Error as e:
        print(f"\nAn error occurred: {e}")
        connection.rollback() # Rollback changes in case of error
    finally:
        if cursor:
            cursor.close()

def create_database():
    # Connect to MySQL
    try:
        path = os.path.join(os.path.dirname(__file__)) + "\\"
        conn = mysql.connector.connect(host=HOSTNAME, user=USERNAME, password=PASSWORD)
        if conn.is_connected():
            execute_sql_file(path + FILENAME, conn)

    except Error as e:
        print(f"Error connecting to MySQL: {e}")

    finally:
        if conn and conn.is_connected():
            conn.close()

if __name__ == "__main__":
    create_database()