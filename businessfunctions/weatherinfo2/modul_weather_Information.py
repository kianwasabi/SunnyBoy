from datetime import datetime
import pytz
from timezonefinder import TimezoneFinder
from .class_def import WeatherInformation, API

def modulWeatherInfo(city_name:str, user_api:str): 
    '''
    Generates weatherinformation for a given location.
    :param cityname: (str) Name of the City
    :param user_api: (str) API Key for openweathermaps.com
    :return: (turpel) objects of class WeatherInformation & API Error Code
    '''
    api_call = API(city_name,user_api)
    api_data = api_call.api_data
    api_error = api_call.error_code
    # extract information
    latitude            = api_data['coord']['lat']
    longitude           = api_data['coord']['lon']
    temperatur          = round(((api_data['main']['temp'])-273.15),3) #°F to °C
    weather_description = api_data['weather'][0]['description']
    timezone            = api_data['timezone'] #timezone in seconds unix, UTC
    timezone_at         = TimezoneFinder().timezone_at(lng=longitude,lat=latitude)
    tz                  = pytz.timezone(timezone_at)
    time_in_tz          = datetime.now(tz)
    timestamp_sunrise   = api_data['sys']['sunrise'] #timezone in seconds unix, UTC
    timestamp_sunrise   = timestamp_sunrise + (timezone-7200) # edit sunrise time in timezone 
    timestamp_sunrise   = datetime.fromtimestamp(timestamp_sunrise)
    timestamp_sunset    = api_data['sys']['sunset']
    timestamp_sunset    = timestamp_sunset + (timezone-7200)
    timestamp_sunset    = datetime.fromtimestamp(timestamp_sunset)
    timezone            = round(api_data['timezone']/60/60) #timezone shifted in seconds, unix, UTC
    cloudiness          = api_data['clouds']['all']
    visibility          = api_data['visibility']
    wind_speed          = api_data['wind']['speed']
    wind_direction      = api_data['wind']['deg']
    # construct  
    weatherinfo = WeatherInformation(timestamp_sunrise=timestamp_sunrise,timestamp_sunset=timestamp_sunset,
        temperatur=temperatur,weather_descr=weather_description,cloudiness=cloudiness,
        visibility=visibility,wind_speed=wind_speed,wind_direction=wind_direction,
        name=city_name,longitude=longitude,latitude=latitude,timestamp=time_in_tz,timezone=timezone)
    return weatherinfo