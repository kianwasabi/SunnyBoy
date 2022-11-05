#import packages 
from weatherinfo.modul_weather_Information import *
from app.routes import *
from database.db import *

def main(): 
    #create databases
    sql_creat_sunposition_table = '''
        CREATE TABLE IF NOT EXISTS sunpositions (
            sid INTEGER PRIMARY KEY AUTOINCREMENT,
            sazimuth TEXT NOT NULL,
            selevation TEXT NOT NULL,
            ssunrise TEXT NOT NULL,
            ssunset TEXT NOT NULL
            ); '''
    create_db_table(sql_creat_sunposition_table)

    #run flask app - creat Web Application with Flask & test locally 😁
    app.run(host="127.0.0.1", port=8080, debug=True) 
    print("🫡Server started")

if __name__ == '__main__':
    main()