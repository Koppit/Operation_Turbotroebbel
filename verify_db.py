import argparse
import sys
from typing import Tuple

try:
    import pymysql
except Exception:
    pymysql = None

try:
    import mysql.connector
except Exception:
    mysql = None


def connect(host: str, user: str, password: str, database: str):
    if pymysql is not None:
        return pymysql.connect(host=host, user=user, password=password, database=database, autocommit=True)
    return mysql.connector.connect(host=host, user=user, password=password, database=database, autocommit=True)


def fetch_counts(conn) -> Tuple[int, int, int]:
    cur = conn.cursor()
    cur.execute('SELECT COUNT(*) FROM study_programs')
    studies = cur.fetchone()[0]
    cur.execute('SELECT COUNT(*) FROM courses')
    courses = cur.fetchone()[0]
    cur.execute('SELECT COUNT(*) FROM study_place')
    places = cur.fetchone()[0]
    cur.close()
    return studies, courses, places


def fetch_duplicates(conn):
    cur = conn.cursor()
    # duplicate study titles
    cur.execute("SELECT study_title, COUNT(*) AS c FROM study_programs GROUP BY study_title HAVING c>1 ORDER BY c DESC LIMIT 50")
    dup_studies = cur.fetchall()
    # duplicate course ids (shouldn't happen)
    cur.execute("SELECT course_id, COUNT(*) AS c FROM courses GROUP BY course_id HAVING c>1 ORDER BY c DESC LIMIT 50")
    dup_courses = cur.fetchall()
    cur.close()
    return dup_studies, dup_courses


def fetch_per_location(conn):
    cur = conn.cursor()
    cur.execute("SELECT sp.location_id, IFNULL(st.location_name, '') AS location_name, COUNT(*) AS programs FROM study_programs sp LEFT JOIN study_place st ON sp.location_id=st.location_id GROUP BY sp.location_id, st.location_name ORDER BY programs DESC")
    rows = cur.fetchall()
    # count programs without location
    cur.execute('SELECT COUNT(*) FROM study_programs WHERE location_id IS NULL')
    no_loc = cur.fetchone()[0]
    cur.close()
    return rows, no_loc


def main():
    parser = argparse.ArgumentParser(description='Verify DB contents and return basic stats')
    parser.add_argument('--host', default='127.0.0.1')
    parser.add_argument('--user', default='turbotroebbel')
    parser.add_argument('--password', default='turbotroebbel')
    parser.add_argument('--database', default='fagskolen')
    args = parser.parse_args()

    try:
        conn = connect(args.host, args.user, args.password, args.database)
    except Exception as e:
        print('Connection error:', e)
        sys.exit(2)

    try:
        studies, courses, places = fetch_counts(conn)
        print('Database:', args.database)
        print('- Studies (study_programs):', studies)
        print('- Courses (courses):', courses)
        print('- Locations (study_place rows):', places)
        # Duplicates
        dup_studies, dup_courses = fetch_duplicates(conn)
        print('\nDuplicate study titles (top):')
        if dup_studies:
            for title, c in dup_studies:
                print(f'  {c:4d}  {title}')
        else:
            print('  None')

        print('\nDuplicate course_ids (if any):')
        if dup_courses:
            for cid, c in dup_courses:
                print(f'  {c:4d}  {cid}')
        else:
            print('  None')

        # Per-location program counts
        rows, no_loc = fetch_per_location(conn)
        print('\nPrograms per location (top):')
        for loc_id, loc_name, num in rows[:30]:
            disp = loc_name if loc_name else '(no name)'
            print(f'  {num:4d}  id={loc_id}  {disp}')
        print(f'\nPrograms without location_id: {no_loc}')
    except Exception as e:
        print('Query error:', e)
        sys.exit(3)
    finally:
        try:
            conn.close()
        except Exception:
            pass


if __name__ == '__main__':
    main()
