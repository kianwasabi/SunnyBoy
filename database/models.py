#from database import models
import sqlite3
from sqlite3 import Error
import os
from weatherinfo.modul_weather_Information import *

def connect_to_db():
    conn = None
    try:
        conn = sqlite3.connect(f"{os.path.dirname(os.path.abspath(__file__))}/database.db")
    except Error as e:
        print(f"👎 Connection to DB failed. Error: {e}")
    return conn

def drop_db_table():  
    '''
    Drops all tables in database. 
    '''
    try: 
        conn = connect_to_db()
        cur = conn.cursor()
        sql_query = "SELECT name FROM sqlite_schema WHERE type='table' ORDER BY name;"
        cur.execute(sql_query)
        list_tablenames = cur.fetchall() #returns list of tuples
        for list in list_tablenames:
            for tuple in list:
                sql_query = f"DROP TABLE IF EXISTS {tuple};"
                cur.execute(sql_query)    
        conn.commit()
        print(f"👍 Tables droped successfully.")
        conn.close()
    except Error as e: 
        print(f"👎 Dropping tables failed. Error:{e}")

def create_db_table(filename_schema:str, filename_recipescript:str):
    ''' 
    create database and insert device recipes
    :param filename_schema: filename of schema
    :param filename_recipescript: filename of recipe script
    '''
    try:
        conn = connect_to_db()
        cur = conn.cursor()
        with open(f"{os.path.dirname(os.path.abspath(__file__))}/{filename_schema}") as f:
            cur.executescript(f.read())
        print("👍 Tables created successfully.")
        conn.commit()
        conn.close()
    except Error as e:
        print(f"👎 Create tables failed. Error:{e}")

    try: 
        conn = connect_to_db()
        cur = conn.cursor()
        with open(f"{os.path.dirname(os.path.abspath(__file__))}/{filename_recipescript}") as f:
            cur.executescript(f.read())
        print("👍 Recipe saved into database.")
        conn.commit()
        conn.close()
    except Error as e:
        print(f"👎 Saving Recipe failed. Error:{e}")        

def get_recipe_by_device_id(device_id):
    ''' 
    get device recipe from database
    :param filename_schema: filename of schema
    :param filename_recipescript: filename of recipe script
    '''
    recipe_list = []
    #try:
    conn = connect_to_db()
    conn.row_factory = sqlite3.Row
    sql = "SELECT step.http_typ,step.step FROM step WHERE step.step_id IN (SELECT recipe_step.fk_step FROM recipe_step WHERE recipe_step.fk_recipe = (SELECT device.fk_recipe_to_device FROM device WHERE device.device_id = ?))"
    args = (device_id,)
    cur = conn.cursor()
    cur = conn.execute(sql,args)
    rows = cur.fetchall()
    for i in rows:
        tuple_in_recipe_list = {}
        tuple_in_recipe_list["http_typ"] = i["http_typ"]
        tuple_in_recipe_list["step"] = i["step"]
        recipe_list.append(tuple_in_recipe_list)
    #except Error as e:
        #print(f"👎 Fetch Recipe failed. Error: {e}")
    #finally:
    conn.close()
    return recipe_list

def refresh_weatherinformation(): 
    '''
        Uses weatherinfo package to insert current weather data to database
    '''
    #inserted_weatherinformation = {}
    weather, wind, sun = modulWeatherInfo()
    weatherinformation = {
    'locationname' : weather.getLocationName(),
    'longitude' : weather.getLongitude(), 
    'latitude' :weather.getLatitude(),
    'location_time' : weather.getTime(),
    'timezone' : weather.getTimezone(),
    'azimuth': sun.getAzimuth(),
    'elevation': sun.getElevation(),
    'sunrise': sun.getTimeSunrise(),
    'sunset' : sun.getTimeSunset(), 
    'wind_speed': wind.getWindSpeed(),
    'wind_direction': wind.getDirectionPoint(),
    'temperatur': weather.getTemperatur(), 
    'cloudiness': weather.getCloudiness(), 
    'weather_description': weather.getWeatherDiscription(),
    'visibility': weather.getVisibility()
    }
    try:
        conn = connect_to_db()
        cur = conn.cursor()
        sql = "INSERT INTO weatherinformation (locationname, longitude, latitude, location_time, timezone, azimuth, elevation, sunrise, sunset, wind_speed, wind_direction, temperatur, cloudiness, weather_description, visibility) VALUES (?,?,?,?,?,?,?,?,?,?,?,?,?,?,?)"
        args = (weatherinformation['locationname'], weatherinformation['longitude'], weatherinformation['latitude'], weatherinformation['location_time'], weatherinformation['timezone'], weatherinformation['azimuth'], weatherinformation['elevation'], weatherinformation['sunrise'], weatherinformation['sunset'], weatherinformation['wind_speed'],  weatherinformation['wind_direction'], weatherinformation['temperatur'], weatherinformation['cloudiness'], weatherinformation['weather_description'],weatherinformation['visibility'])
        cur.execute(sql,args)
        conn.commit()
        inserted_weatherinformation = get_weatherinformation_by_id(cur.lastrowid)
        #print(f"⏏︎ {cur.rowcount} record inserted. {inserted_weatherinformation}")
        print(f"⏏︎ {cur.rowcount} weather record inserted into database.")
    except Error as e:
        print(f"👎 Insert into database failed. Error: {e}")
    finally:
        conn.close()
    return inserted_weatherinformation

def get_current_weatherinformation():
    weatherinformation = {}
    try:
        conn = connect_to_db()
        conn.row_factory = sqlite3.Row
        cur = conn.cursor()
        weatherinformation = get_weatherinformation_by_id(cur.lastrowid)
        print(cur.lastrowid)
    except Error as e:  
        print(f"👎 Get weatherinfos from database failed. Error: {e}")
    finally:
        conn.close()
    return weatherinformation

def get_weatherinformation_by_id(weatherinformation_id):
    weatherinformation = {}
    try:
        conn = connect_to_db()
        conn.row_factory = sqlite3.Row
        cur = conn.cursor()
        cur.execute("SELECT * FROM weatherinformation WHERE weather_id = ?", (weatherinformation_id,))
        row = cur.fetchone()
        # convert row object to dictionary
        weatherinformation['weather_id'] = row['weather_id']
        weatherinformation['locationname'] = row['locationname']
        weatherinformation['longitude'] = row['longitude'] 
        weatherinformation['latitude'] = row['latitude']
        weatherinformation['location_time'] = row['location_time']
        weatherinformation['timezone'] = row['timezone']
        weatherinformation['azimuth'] = row['azimuth']
        weatherinformation['elevation'] = row['elevation']
        weatherinformation['sunrise'] = row['sunrise']
        weatherinformation['sunset'] = row['sunset']
        weatherinformation['wind_speed'] = row['wind_speed'] 
        weatherinformation['wind_direction'] = row['wind_direction']
        weatherinformation['temperatur'] = row['temperatur']
        weatherinformation['cloudiness'] = row['cloudiness']
        weatherinformation['weather_description'] = row ['weather_description'] 
        weatherinformation['visibility'] = row ['visibility']
    except:
        weatherinformation = {}
    finally:
        conn.close()
    return weatherinformation

def get_current_sunposition():
    #sunposition = []
    sunposition = {}
    try:
        conn = connect_to_db()
        conn.row_factory = sqlite3.Row
        cur = conn.cursor()
        sunposition = get_sunposition_by_id(cur.lastrowid)
    except Error as e:  
        print(f"👎 Get from database failed. Error: {e}")
    finally:
        conn.close()
    return sunposition

def get_sunposition_by_id():
    #sunposition = []
    sunposition = {}
    try:
        conn = connect_to_db()
        conn.row_factory = sqlite3.Row
        cur = conn.cursor()
        cur.execute("SELECT azimuth, elevation FROM weatherinformation")
        rows = cur.fetchall()
        for i in rows:
            #sunposition = {}
            sunposition["azimuth"] = i["azimuth"]
            sunposition["elevation"] = i["elevation"]
            sunposition.append(sunposition)
    except Error as e:
        print(f"👎 Get sunposition from database failed. Error: {e}")
    return sunposition

def post_panelposition(val1,val2):
    panelposition = [val1, val2]
    try:
        conn = connect_to_db()
        conn.row_factory = sqlite3.Row
        cur = conn.cursor()
        sql = "INSERT INTO solarpanel (val1,val2) VALUES (?,?)"
        args = panelposition
        cur.execute(sql,args)
        conn.commit()
    except Error as e:
        print(f"👎 Insert into database failed. Error: {e}")
    return panelposition


# def get_sunposition():
#     sunposition = []
#     try:
#         conn = connect_to_db()
#         conn.row_factory = sqlite3.Row
#         cur = conn.cursor()
#         cur.execute("SELECT azimuth, elevation FROM weatherinformation")
#         rows = cur.fetchall()
#         for i in rows:
#             sunposition = {}
#             sunposition["azimuth"] = i["azimuth"]
#             sunposition["elevation"] = i["elevation"]
#             sunposition.append(sunposition)
#     except:
#         sunposition = []
#     return sunposition

# def insert_sunposition(suninfo):
#     inserted_sunposition = {}
#     try:
#         conn = connect_to_db()
#         cur = conn.cursor()
#         sql = "INSERT INTO sunpositions (sazimuth, selevation, ssunrise, ssunset) VALUES (?,?,?,?)"
#         val = (suninfo['azimuth'], suninfo['elevation'], suninfo['sunrise'], suninfo['sunset'])
#         cur.execute(sql,val)
#         conn.commit()
#         inserted_sunposition = get_sunposition_by_sid(cur.lastrowid)
#         print("⏏︎ ",cur.rowcount, "record inserted.","/",inserted_sunposition)
#     except Error as e:
#         print("🥲 insert into database failed.")
#         print(e)
#         #conn.rollback()
#     finally:
#         conn.close()

#     return inserted_sunposition


# def get_sunpositions():
#     sunpositions = []
#     try:
#         conn = connect_to_db()
#         conn.row_factory = sqlite3.Row
#         cur = conn.cursor()
#         cur.execute("SELECT * FROM sunpositions")
#         rows = cur.fetchall()

#         # convert row objects to dictionary
#         for i in rows:
#             sunposition = {}
#             sunposition["sid"] = i["sid"]
#             sunposition["sazimuth"] = i["sazimuth"]
#             sunposition["selevation"] = i["selevation"]
#             sunposition["ssunrise"] = i["ssunrise"]
#             sunposition["ssunset"] = i["ssunset"]
#             sunpositions.append(sunposition)

#     except:
#         sunpositions = []

#     return sunpositions


# def get_sunposition_by_sid(sunposition_sid):
#     sunposition = {}
#     try:
#         conn = connect_to_db()
#         conn.row_factory = sqlite3.Row
#         cur = conn.cursor()
#         cur.execute("SELECT * FROM sunpositions WHERE sid = ?", (sunposition_sid,))
#         row = cur.fetchone()

#         # convert row object to dictionary
#         sunposition["sid"] = row["sid"]
#         sunposition["sazimuth"] = row["sazimuth"]
#         sunposition["selevation"] = row["selevation"]
#         sunposition["ssunrise"] = row["ssunrise"]
#         sunposition["ssunset"] = row["ssunset"]
#     except:
#         sunposition = {}

#     return sunposition


# def update_sunposition(sunposition):
#     updated_sunposition = {}
#     try:
#         conn = connect_to_db()
#         cur = conn.cursor()
#         cur.execute("UPDATE sunpositions SET sazimuth = ?, selevation = ?, ssunrise = ?, ssunset = ? WHERE sid =?", (sunposition["sazimuth"], sunposition["selevation"], sunposition["ssunrise"], sunposition["ssunset"], sunposition["sid"]))
#         conn.commit()
#         #return the sunposition
#         updated_sunposition = get_sunposition_by_sid(sunposition["sid"])

#     except:
#         conn.rollback()
#         updated_sunposition = {}
#     finally:
#         conn.close()

#     return updated_sunposition


# def delete_sunposition(sunposition_sid):
#     message = {}
#     try:
#         conn = connect_to_db()
#         conn.execute("DELETE from updated_sunpositions WHERE sid = ?", (sunposition_sid))
#         conn.commit()
#         message["status"] = "Sun Position deleted successfully"
#     except:
#         conn.rollback()
#         message["status"] = "Cannot delete Sun Position"
#     finally:
#         conn.close()

#     return message