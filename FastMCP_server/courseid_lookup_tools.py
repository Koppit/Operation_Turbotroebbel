import mysql.connector
from database_connection import DBConnection

"""
Methods for quering the Study Courses lookup table, to be exposed as tools in the MCP Server
"""

class TableStudyCoursesLookup:
    def __init__(self, conn: DBConnection, table: str):
        self.conn = conn
        self.table = table
    
    def get_study_program_courseIDs(self, study_title: str) -> list:
        """
        One-line: Return distinct course IDs for a specific study program.

        Parameters:
            study_title (str): The title of the study program (exact match).

        Returns:
            dict: {"status":"success"|"error", "result": list[str], "error_message": str (optional)}

        Example:
            {"status":"success", "result":["01TD01B","02TD02A"]}

        Notes:
            - Use parameterized queries to avoid SQL injection.
        """
        results = self.conn.query(f"SELECT DISTINCT course_id FROM {self.table} WHERE study_title = '{study_title}'")
        if not results:
            return {"status":"error", "error_message":"Study program not found"}
        return {"status":"success", "result": [result[0] for result in results]}
    
   
    
if __name__ == "__main__":
    DATABASE = "fagskolen"
    STUDY_PROGRAM_COURSE_ID_TABLE = "lookuptalbe_study_course"

    # verify method outputs
    try:
        db_conn = DBConnection()
        programs = TableStudyCoursesLookup(db_conn, f"{DATABASE}.{STUDY_PROGRAM_COURSE_ID_TABLE}")

        results = programs.get_study_program_courseIDs("Elkraft")
        
        print(results)

    except mysql.connector.Error as err:
        print(f"Error: {err}")