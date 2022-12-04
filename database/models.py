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
    :param:
    :return:
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
    :param device_id: device id from request
    :return: recipe list
    '''
    recipe = {}
    http_typ = {}
    step = {}
    try:
        conn = connect_to_db()
        #conn.row_factory = sqlite3.Row
        sql = "SELECT step.http_typ,step.step           \
                FROM step                               \
                WHERE step.step_id IN                   \
                (SELECT recipe_step.fk_step             \
                FROM recipe_step                        \
                WHERE recipe_step.fk_recipe =           \
                    (SELECT device.fk_recipe_to_device  \
                    FROM device                         \
                    WHERE device.device_id = ?))"
        args = (device_id,)
        cur = conn.cursor()
        cur = conn.execute(sql,args)
        rows = cur.fetchall()
        for i, item in enumerate(rows):
            #element_http_typ = {f"{i}":item["http_typ"]}
            element_http_typ = {f"{i}":item[0]}
            http_typ.update(element_http_typ)
            #element_step = {f"{i}":item["step"]}
            element_step = {f"{i}":item[1]}
            step.update(element_step)
    except Error as e:
        print(f"👎 Fetch Recipe failed. Error: {e}")
    finally:
        conn.close()
        recipe["http_typ"] = http_typ
        recipe["step"] = step
    return recipe

def refresh_weatherinformation(): 
    '''
        Insert current weather data to database by using weatherinfo package. 
        :param: none
        :return: inserted weatherinformation & timestamp 
    '''
    inserted_weatherinformation = {}
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
        sql = "INSERT INTO weatherinformation           \
                (locationname, longitude, latitude,     \
                location_time, timezone, azimuth,       \
                elevation, sunrise, sunset,             \
                wind_speed, wind_direction, temperatur, \
                cloudiness, weather_description,        \
                visibility)                             \
                VALUES (?,?,?,?,?,?,?,?,?,?,?,?,?,?,?)"
        args = (weatherinformation['locationname'],     
                weatherinformation['longitude'],        
                weatherinformation['latitude'],          
                weatherinformation['location_time'],     
                weatherinformation['timezone'],  
                weatherinformation['azimuth'], 
                weatherinformation['elevation'],  
                weatherinformation['sunrise'],  
                weatherinformation['sunset'],  
                weatherinformation['wind_speed'],   
                weatherinformation['wind_direction'],  
                weatherinformation['temperatur'], 
                weatherinformation['cloudiness'],  
                weatherinformation['weather_description'],  
                weatherinformation['visibility'])
        cur.execute(sql,args)
        conn.commit()
        inserted_weatherinformation = get_weatherinformation_by_id(cur.lastrowid)
        print(f"⏏︎ {cur.rowcount} weather record inserted into database.")
    except Error as e:
        print(f"👎 Insert into database failed. Error: {e}")
    finally:
        conn.close()
    return inserted_weatherinformation, datetime.now()

def get_current_weatherinformation():
    weatherinformation = {}
    try:
        weatherinformation = get_weatherinformation_by_id("MAX")
    except Error as e:  
        print(f"👎 Getting weatherinformations from database failed. Error: {e}")
    return weatherinformation

def get_weatherinformation_by_id(weatherinformation_id):
    weatherinformation = {}
    try:
        conn = connect_to_db()
        cur = conn.cursor()
        if weatherinformation_id ==  "MAX":
            sql = "SELECT * FROM weatherinformation WHERE weather_id = (SELECT MAX(weather_id) FROM weatherinformation);"
            cur.execute(sql) 
        else:
            sql = "SELECT * FROM weatherinformation WHERE weather_id = ?;"
            args = (weatherinformation_id,)
            cur.execute(sql,args)
        row = cur.fetchone()
        # convert row object to dictionary
        weatherinformation['weather_id']            = row[0]
        weatherinformation['locationname']          = row[1]
        weatherinformation['longitude']             = row[2] 
        weatherinformation['latitude']              = row[3]
        weatherinformation['location_time']         = row[4]
        weatherinformation['timezone']              = row[5]
        weatherinformation['azimuth']               = row[6]
        weatherinformation['elevation']             = row[7]
        weatherinformation['sunrise']               = row[8]
        weatherinformation['sunset']                = row[9]
        weatherinformation['wind_speed']            = row[10] 
        weatherinformation['wind_direction']        = row[11]
        weatherinformation['temperatur']            = row[12]
        weatherinformation['cloudiness']            = row[13]
        weatherinformation['weather_description']   = row [14] 
        weatherinformation['visibility']            = row [15]
    except:
        weatherinformation = {}
    finally:
        conn.close()
    return weatherinformation

def get_current_sunposition():
    sunposition = {}
    try:
        sunposition = get_sunposition_by_id("MAX")
    except Error as e:  
        print(f"👎 Get current sunposition from database failed. Error: {e}")
    return sunposition

def get_sunposition_by_id(sunposition_id):
    sunposition = {}
    try:
        conn = connect_to_db()
        cur = conn.cursor()
        if sunposition_id == "MAX": 
            sql = "SELECT azimuth,elevation FROM weatherinformation WHERE weather_id = \
                    (SELECT MAX(weather_id) FROM weatherinformation);"
            cur.execute(sql)
        else: 
            sql = "SELECT azimuth, elevation FROM weatherinformation WHERE weather_id = ?"
            args = (sunposition_id,)
            cur.execute(sql,args)
        row = cur.fetchone()
        #row to dict
        sunposition['azimuth'] = row[0]
        sunposition['elevation'] = row[1]
    except Error as e:
        print(f"👎 Get sunposition by id from database failed. Error: {e}")
    return sunposition

def post_panelposition(val1,val2):
    panelposition = (val1, val2)
    try:
        conn = connect_to_db()
        #conn.row_factory = sqlite3.Row
        cur = conn.cursor()
        sql = "INSERT INTO solarpanel (value1,value2) VALUES (?,?)"
        args = panelposition
        cur.execute(sql,args)
        conn.commit()
    except Error as e:
        print(f"👎 Insert into database failed. Error: {e}")
    finally:
        conn.close()
    return panelposition, datetime.now()