#include libraries
import os
import os.path
import requests
import PySimpleGUI as sg
from datetime import datetime
import pytz
from timezonefinder import TimezoneFinder
# import classes
from sun_def import Sun 
from weather_def import Weather
from wind_def import Wind
 
#clear interpreter console
os.system('cls' if os.name == 'nt' else 'clear')

def callOpenWeatherAPI(city_name):
    def apiLogin (): 
        filename = 'OpenWeatherMap.txt'  
        try:
            with open(filename) as file:
                lines = file.readlines()
            user_api = lines[-1]
            return user_api
        except FileNotFoundError as err: 
            print(filename,"not found")
            raise SystemExit(err)
        else: 
            return user_api
    user_api = apiLogin()

    #Call OpenWeatherMap API 
    try: 
        complete_api_link = "https://api.openweathermap.org/data/2.5/weather?q="+city_name+"&appid="+user_api
        api_link = requests.get(complete_api_link)
        api_data = api_link.json()
        api_link.raise_for_status()
    except Exception as err: 
            if api_data['cod'] == '404':
                print("Invalide City. Please check city name.")
                raise SystemExit(err)
    else: 
        return api_data

def printinTerminal(weather,wind,sun):
    print("---------------------------------------------------------------")
    print("Location: ",weather.getLocationName(),"(",weather.getLongitude(),",",weather.getLatitude(),")")
    print("Time:", weather.getDate(),weather.getTime())
    print("Wind:", wind.getWindSpeed(), "from",wind.getDirectionPoint(),"(",wind.getDirectionDegree(),")")
    print("Sun:", "Position:","(",sun.getAzimuth(),",",sun.getElevation(),")","Sunrise:", sun.getTimeSunrise(),"Sunset",sun.getTimeSunset())
    print("---------------------------------------------------------------")

def main(): 
    #bootcCall API
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
    result = TimezoneFinder().timezone_at(lng=longitude,lat=latitude)
    tz = pytz.timezone(result)
    time_in_tz = datetime.now(tz)
    timestamp_sunrise = api_data['sys']['sunrise']
    timestamp_sunrise = timestamp_sunrise + (timezone-7200)
    timestamp_sunrise = datetime.fromtimestamp(timestamp_sunrise)
    timestamp_sunset = api_data['sys']['sunset']
    timestamp_sunset = timestamp_sunset + (timezone-7200)
    timestamp_sunset = datetime.fromtimestamp(timestamp_sunset)
    timezone = round(api_data['timezone']/60/60) #timezone shifted in seconds from unix, UTC
    cloudiness = api_data['clouds']['all']
    visibility = api_data['visibility']
    wind_speed = api_data['wind']['speed']
    wind_direction = api_data['wind']['deg']
    #Initialization Objects
    weather = Weather(temperatur,weather_description, cloudiness, visibility,cityname, longitude, latitude, time_in_tz, timezone)
    wind = Wind(wind_speed, wind_direction, cityname, longitude, latitude, time_in_tz,timezone)
    sun = Sun(timestamp_sunrise,timestamp_sunset, cityname, longitude, latitude, time_in_tz,timezone)
    #Plot in terminal
    printinTerminal(weather,wind,sun)
    
if __name__ == '__main__':
    main()