#import packages 
from app.routes import *
from database.db import *
import socket

def run(): 
    #create databases
    sql_create_sunposition_table = '''
        CREATE TABLE IF NOT EXISTS sunpositions (
            sid INTEGER PRIMARY KEY AUTOINCREMENT,
            sazimuth TEXT NOT NULL,
            selevation TEXT NOT NULL,
            ssunrise TEXT NOT NULL,
            ssunset TEXT NOT NULL
            ); '''
    create_db_table(sql_create_sunposition_table)

    #get host ip adress
    hostname = socket.gethostname()
    hostIP = socket.gethostbyname(hostname)
    #start web server & run flask app
    app.run(hostIP, port=8080, debug=True)
    print("🫡Server started")

if __name__ == '__main__':
    run()