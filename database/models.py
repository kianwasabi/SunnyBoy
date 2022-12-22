#from database import models
import sqlite3
from sqlite3 import Error
import os
from weatherinfo.modul_weather_Information import *

def connect_to_db():
    '''
    Connect to database. 
    :param: none
    :return: none
    '''
    conn = None
    filename_database = "database.db"
    try:
        conn = sqlite3.connect(f"{os.path.dirname(os.path.abspath(__file__))}/{filename_database}")
    except Error as e:
        print(f"👎 Connection to {filename_database} failed. Error: {e}")
    return conn

def drop_db_table():  
    '''
    Drops all tables in database. 
    :param: none
    :return: none
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
    :param filename_schema: (str) filename of schema
    :param filename_recipescript: (str) filename of recipe script
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
    method = {}
    route = {}
    key = {}
    reqkeys = {} #keys in dict for request message
    reskeys = {} #keys in dict for response message
    try:
        conn = connect_to_db()
        sql_step =   "SELECT \
                step.step_id, \
                step.method, \
                step.route       \
                FROM step \
                JOIN recipe_step \
                ON recipe_step.fk_step = step.step_id\
                JOIN recipe \
                ON recipe.recipe_id = recipe_step.fk_recipe\
                JOIN device \
                ON recipe.recipe_id=device.fk_recipe_to_device\
                WHERE device.device_id = ?"
        args = (device_id,)

        sql_req =   "SELECT \
                requestkey.keytitle\
                FROM step_requestkey  \
                JOIN requestkey  \
                ON requestkey.requestkey_id=step_requestkey.fk_requestkey\
                WHERE step_requestkey.fk_step = ?"         

        sql_res = "SELECT \
                responsekey.keytitle\
                FROM step_responsekey\
                JOIN responsekey\
                ON responsekey.responsekey_id=step_responsekey.fk_responsekey\
                WHERE step_responsekey.fk_step = ?"

        cur = conn.cursor()
        cur = conn.execute(sql_step,args)
        rows = cur.fetchall()
        for i, item in enumerate(rows):
            #step key
            element_key = {f"{i}":item[0]}
            key.update(element_key)
            #step method
            element_method = {f"{i}":item[1]}
            method.update(element_method)
            #step route
            element_route = {f"{i}":item[2]}
            route.update(element_route)
        
        for i, val in enumerate(key.values()):
            #step req keys dict
            cur = conn.execute(sql_req,(val,)) 
            ele = cur.fetchall()
            element_reqkey = {f"{i}":ele}
            reqkeys.update(element_reqkey)
            #step res keys dict
            cur = conn.execute(sql_res,(val,)) 
            ele = cur.fetchall()
            element_reskey = {f"{i}":ele}
            reskeys.update(element_reskey)

    except Error as e:
        print(f"👎 Fetch Recipe failed. Error: {e}")
    finally:
        conn.close()
        recipe["domain"] = "domain=header['Device']"
        recipe["method"] = method
        recipe["route"]  = route
        recipe["key"]  = key
        recipe["request"] = reqkeys
        recipe["response"] = reskeys
        
    return recipe

def refresh_weatherinformation(): 
    '''
    Insert current weather data to database by using weatherinfo package. 
    :param: none
    :return: inserted weatherinformation & timestamp 
    '''
    inserted_weatherinformation = {}
    cityname = "Braunschweig"
    user_api = "4b8f1ddd0540ebd49a6b0ca7927e3534"
    weather, wind, sun = modulWeatherInfo(cityname,user_api)
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
    '''
    Returns the most recent weatherinformation from the database.
    :param: none
    :return weatherinformation : current weatherinformation
    '''
    weatherinformation = {}
    try:
        weatherinformation = get_weatherinformation_by_id("MAX")
    except Error as e:  
        print(f"👎 Getting weatherinformations from database failed. Error: {e}")
    return weatherinformation

def get_weatherinformation_by_id(weatherinformation_id):
    '''
    Returns weatherinformation by id from database.
    :param weatherinformation_id: (int) id in database
    :return weatherinformation: weatherinformation by id
    '''
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
    '''
    Returns the most recent sunposition from the weatherinformation table.
    :param: none
    :return weatherinformation : current weatherinformation
    '''
    sunposition = {}
    try:
        sunposition = get_sunposition_by_id("MAX")
    except Error as e:  
        print(f"👎 Get current sunposition from database failed. Error: {e}")
    return sunposition

def get_sunposition_by_id(sunposition_id):
    '''
    Returns sunposition by id from database.
    :param sunposition_id: (int) id in database
    :return sunposition: sunposition by id
    '''
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
    '''
    Saves the received adjustments to the solar panel to the database.
    :param val1: Value 1
    :param val2: Value 2
    :return panelposition : adjusted panelposition
    :return datetime.now(): Timestamp
    '''
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