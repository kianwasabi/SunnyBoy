import sqlite3
from sqlite3 import Error

def connect_to_db():
    conn = None
    try:
        conn = sqlite3.connect('database.db')
    except Error as e:
        print("🥲 Connection to DB failed.")
        print(e)
    return conn


def create_db_table(create_table_sql):
    try:
        conn = connect_to_db()
        cur = conn.cursor()
        cur.execute(create_table_sql)
        conn.commit()
        print("😁 Table created successfully.")
    except Error as e:
        print("🥲 Sun Position creation failed.")
        print(e)
    finally:
        conn.close()


def insert_sunposition(suninfo):
    inserted_sunposition = {}
    try:
        conn = connect_to_db()
        cur = conn.cursor()
        sql = "INSERT INTO sunpositions (sazimuth, selevation, ssunrise, ssunset) VALUES (?,?,?,?)"
        val = (suninfo['azimuth'], suninfo['elevation'], suninfo['sunrise'], suninfo['sunset'])
        cur.execute(sql,val)
        conn.commit()
        inserted_sunposition = get_sunposition_by_sid(cur.lastrowid)
        print("⏏︎ ",cur.rowcount, "record inserted.","/",inserted_sunposition)
    except Error as e:
        print("🥲 insert into database failed.")
        print(e)
        #conn.rollback()
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
            sunposition["ssunrise"] = i["ssunrise"]
            sunposition["ssunset"] = i["ssunset"]
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
        sunposition["ssunrise"] = row["ssunrise"]
        sunposition["ssunset"] = row["ssunset"]
    except:
        sunposition = {}

    return sunposition


def update_sunposition(sunposition):
    updated_sunposition = {}
    try:
        conn = connect_to_db()
        cur = conn.cursor()
        cur.execute("UPDATE sunpositions SET sazimuth = ?, selevation = ?, ssunrise = ?, ssunset = ? WHERE sid =?", (sunposition["sazimuth"], sunposition["selevation"], sunposition["ssunrise"], sunposition["ssunset"], sunposition["sid"]))
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