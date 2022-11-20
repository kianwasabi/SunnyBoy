#include libraries
import os
import os.path
from datetime import datetime
import pytz
from timezonefinder import TimezoneFinder
from .weatherAPI_call import callOpenWeatherAPI
from .sun_def import Sun 
from .weather_def import Weather
from .wind_def import Wind


def printinTerminal(weather,wind,sun):
    #clear interpreter console
    #os.system('cls' if os.name == 'nt' else 'clear')
    print("---------------------------------------------------------------")
    print("Location:",weather.getLocationName(),"(",weather.getLongitude(),";",weather.getLatitude(),")")
    print("Time:",weather.getDate(),weather.getTime())
    print("Wind:",wind.getWindSpeed(),"from",wind.getDirectionPoint(),"(",wind.getDirectionDegree(),")")
    print("Sun:","Position:","(",sun.getAzimuth(),";",sun.getElevation(),")","Sunrise:",sun.getTimeSunrise(),"Sunset:",sun.getTimeSunset())
    print("---------------------------------------------------------------")

def modulWeatherInfo(): 
    #Call API
    #cityname = input("Enter city name: ")
    cityname = "Braunschweig"
    api_data = callOpenWeatherAPI(cityname)
    latitude = api_data['coord']['lat']
    longitude= api_data['coord']['lon']
    temperatur = ((api_data['main']['temp']) - 273.15) #°F to °C
    weather_description = api_data['weather'][0]['description']
    timezone = api_data['timezone'] #timezone in seconds unix, UTC
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
    return weather,wind,sun