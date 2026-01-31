import mysql.connector
from mysql.connector import Error
import os

HOSTNAME = "127.0.0.1"
USERNAME = "root"
PASSWORD = "admin"
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

# Connect to MySQL
try:
    path = os.path.join(os.path.dirname(__file__))+"\\"
    conn = mysql.connector.connect(host=HOSTNAME, user=USERNAME, password=PASSWORD)
    if conn.is_connected():
        execute_sql_file(path + FILENAME, conn)

except Error as e:
    print(f"Error connecting to MySQL: {e}")

finally:
    if conn and conn.is_connected():
        conn.close()
