import sqlite3
from sqlite3 import Error

def connect_to_db():
    #create a database connection to the SQLite database specified by db_file
    #param db_file: database file
    #return: Connection object or None
    conn = None
    try:
        conn = sqlite3.connect('database.db')
    except Error as e:
        print(e)
    return conn


def create_db_table(conn, create_table_sql):
    #create a table from the create_table_sql statement
    #param conn: Connection object
    #param create_table_sql: a CREATE TABLE statement
    #return: None
    try:
        conn = connect_to_db()
        conn.execute('''DROP TABLE sunpositions''')
        conn.execute('''
            CREATE TABLE sunpositions (
                sid INTEGER PRIMARY KEY NOT NULL,
                sazimuth TEXT NOT NULL,
                selevation TEXT NOT NULL,
                sdate TEXT NOT NULL,
                stime TEXT NOT NULL
            );
        ''')

        conn.commit()
        print("Sun Position table created successfully")
    except:
        print("Sun Position creation failed - Maybe table")
    finally:
        conn.close()


def insert_sunposition(sunposition):
    inserted_sunposition = {}
    try:
        conn = connect_to_db()
        cur = conn.cursor()
        cur.execute("INSERT INTO sunposition (sazimuth, selevation, sdate, stime) VALUES (?, ?, ?, ?)", (sunposition['sazimuth'], sunposition['selevation'], sunposition['sdate'], sunposition['stime']))
        conn.commit()
        inserted_sunposition = get_sunposition_by_sid(cur.lastrowid)
    except:
        conn().rollback

    finally:
        conn.close()

    return inserted_sunposition


def get_sunpositions():
    sunpositions = []
    try:
        conn = connect_to_db()
        conn.row_factory = sqlite3.Row
        cur = conn.cursor()
        cur.execute("SELECT * FROM sunpositions")
        rows = cur.fetchall()

        # convert row objects to dictionary
        for i in rows:
            sunposition = {}
            sunposition["sid"] = i["sid"]
            sunposition["sazimuth"] = i["sazimuth"]
            sunposition["selevation"] = i["selevation"]
            sunposition["sdate"] = i["sdate"]
            sunposition["stime"] = i["stime"]
            sunpositions.append(sunposition)

    except:
        sunpositions = []

    return sunpositions


def get_sunposition_by_sid(sunposition_sid):
    sunposition = {}
    try:
        conn = connect_to_db()
        conn.row_factory = sqlite3.Row
        cur = conn.cursor()
        cur.execute("SELECT * FROM sunpositions WHERE sid = ?", (sunposition_sid,))
        row = cur.fetchone()

        # convert row object to dictionary
        sunposition["sid"] = row["sid"]
        sunposition["sazimuth"] = row["sazimuth"]
        sunposition["selevation"] = row["selevation"]
        sunposition["sdate"] = row["sdate"]
        sunposition["stime"] = row["stime"]
    except:
        sunposition = {}

    return sunposition


def update_sunposition(sunposition):
    updated_sunposition = {}
    try:
        conn = connect_to_db()
        cur = conn.cursor()
        cur.execute("UPDATE sunpositions SET sazimuth = ?, selevation = ?, sdate = ?, stime = ? WHERE sid =?", (sunposition["sazimuth"], sunposition["selevation"], sunposition["sdate"], sunposition["stime"], sunposition["sid"]))
        conn.commit()
        #return the sunposition
        updated_sunposition = get_sunposition_by_sid(sunposition["sid"])

    except:
        conn.rollback()
        updated_sunposition = {}
    finally:
        conn.close()

    return updated_sunposition


def delete_sunposition(sunposition_sid):
    message = {}
    try:
        conn = connect_to_db()
        conn.execute("DELETE from updated_sunpositions WHERE sid = ?", (sunposition_sid))
        conn.commit()
        message["status"] = "Sun Position deleted successfully"
    except:
        conn.rollback()
        message["status"] = "Cannot delete Sun Position"
    finally:
        conn.close()

    return message