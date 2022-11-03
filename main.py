#include libraries
import os
import os.path
#import PySimpleGUIWeb as sg
from datetime import datetime
import pytz
from timezonefinder import TimezoneFinder


# import classes & modules from src
from src.weatherAPI_call import callOpenWeatherAPI
from src.sun_def import Sun 
from src.weather_def import Weather
from src.wind_def import Wind


def printinTerminal(weather,wind,sun):
    #clear interpreter console
    os.system('cls' if os.name == 'nt' else 'clear')
    print("---------------------------------------------------------------")
    print("Location: ",weather.getLocationName(),"(",weather.getLongitude(),",",weather.getLatitude(),")")
    print("Time:", weather.getDate(),weather.getTime())
    print("Wind:", wind.getWindSpeed(), "from",wind.getDirectionPoint(),"(",wind.getDirectionDegree(),")")
    print("Sun:", "Position:","(",sun.getAzimuth(),",",sun.getElevation(),")","Sunrise:", sun.getTimeSunrise(),"Sunset",sun.getTimeSunset())
    print("---------------------------------------------------------------")

def main(): 
    #Call API
    cityname = input("Enter city name: ")
    api_data = callOpenWeatherAPI(cityname)
    latitude = api_data['coord']['lat']
    longitude= api_data['coord']['lon']
    temperatur = ((api_data['main']['temp']) - 273.15) #°F to °C
    weather_description = api_data['weather'][0]['description']
    timezone = api_data['timezone'] #timezone in seconds unix, UTC
    #time_api = api_data['dt'] #api time of data caluclation, timestamp unix, UTC
    #time_in_tz = time_api + timezone
    #time_in_tz = datetime.fromtimestamp(time_in_tz)
    timezone_at = TimezoneFinder().timezone_at(lng=longitude,lat=latitude)
    tz = pytz.timezone(timezone_at)
    time_in_tz = datetime.now(tz)
    timestamp_sunrise = api_data['sys']['sunrise'] #timezone in seconds unix, UTC
    timestamp_sunrise = timestamp_sunrise + (timezone-7200) # edit sunrise time in timezone 
    timestamp_sunrise = datetime.fromtimestamp(timestamp_sunrise)
    timestamp_sunset = api_data['sys']['sunset']
    timestamp_sunset = timestamp_sunset + (timezone-7200)
    timestamp_sunset = datetime.fromtimestamp(timestamp_sunset)
    timezone = round(api_data['timezone']/60/60) #timezone shifted in seconds, unix, UTC
    cloudiness = api_data['clouds']['all']
    visibility = api_data['visibility']
    wind_speed = api_data['wind']['speed']
    wind_direction = api_data['wind']['deg']
    #initialization Objects
    weather = Weather(temperatur,weather_description, cloudiness, visibility,cityname, longitude, latitude, time_in_tz, timezone)
    wind = Wind(wind_speed, wind_direction, cityname, longitude, latitude, time_in_tz,timezone)
    sun = Sun(timestamp_sunrise,timestamp_sunset, cityname, longitude, latitude, time_in_tz,timezone)
    #print in terminal
    printinTerminal(weather,wind,sun) 
    #
# users = []
# user0 = {
#     "name": "Charles Effiong",
#     "email": "charles@gamil.com",
#     "phone": "067765665656",
#     "address": "Lui Str, Innsbruck",
#     "country": "Austria"
# }

# users.append(user0)

#create_db_table()

#for i in sunpositions:
#    print(insert_sunposition(i))

#run flask app
#app.debug = True
#app.run(debug=True)
#app.run()
#app.run(host="127.0.0.1", port=8080, debug=True) #creat Web Application with Flask & test locally

if __name__ == '__main__':
    main()