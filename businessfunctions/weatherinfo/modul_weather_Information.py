from datetime import datetime
import pytz
import requests
from collections import defaultdict
from timezonefinder import TimezoneFinder
from .class_def import WeatherInformation

def def_value_dict():
    return "Not Present"

def callOpenWeatherAPI(city_name:str , user_api:str):
    api_data = defaultdict(def_value_dict)
    try: 
        complete_api_link = "https://api.openweathermap.org/data/2.5/weather?q="+city_name+"&appid="+user_api
        print(complete_api_link)
        response = requests.get(complete_api_link)
        api_data = response.json()
        response.raise_for_status()
        return api_data
    except requests.exceptions.HTTPError as err: 
        #Connected to Server successfully BUT API link was not accepted
        print("HTTP-Error:"+str(api_data['cod'])+" "+api_data['message']+"Invalid input: city name or user api")
        #return api_data
        raise SystemExit(err)
    except (requests.exceptions.ConnectionError, requests.exceptions.ConnectTimeout) as err:
        #Error message when Connection failed/timed out. 
        #city name & user api may be correct but remaining link is incorrect
        print("Connection to api.openweathermaps.org failed.")
        #return api_data
        raise SystemExit(err)

def modulWeatherInfo(cityname:str, user_api:str): 
    '''
    Generates weatherinformation for a given location.
    :param cityname: (str) Name of the City
    :param user_api: (str) API Key for openweathermaps.com
    :return: (turpel) objects of class wind, weather and sun
    '''
    #Call openweahtermaps API
    api_data = callOpenWeatherAPI(cityname,user_api)
    latitude = api_data['coord']['lat']
    longitude= api_data['coord']['lon']
    temperatur = ((api_data['main']['temp']) - 273.15) #°F to °C
    temperatur = round(temperatur,3)
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
    #initialization Object
    weatherinfo = WeatherInformation(timestamp_sunrise=timestamp_sunrise,timestamp_sunset=timestamp_sunset,
    temperatur=temperatur,weather_descr=weather_description,cloudiness=cloudiness,
    visibility=visibility,wind_speed=wind_speed,wind_direction=wind_direction,
    name=cityname,longitude=longitude,latitude=latitude,timestamp=time_in_tz,timezone=timezone)
    return weatherinfo