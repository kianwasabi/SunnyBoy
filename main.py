#import packages 
from weatherinfo.modul_weather_Information import *
from app.routes import *
from database.db import *

def main(): 
    #modulWeatherInfo()
    #run flask app
    app.debug = True
    app.run(debug=True)
    app.run()
    app.run(host="127.0.0.1", port=8080, debug=True) #creat Web Application with Flask & test locally 😁
if __name__ == '__main__':
    main()