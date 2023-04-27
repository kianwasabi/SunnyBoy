import requests 

def modulWeatherInfo(city_name:str, user_api:str): 
    '''
    Generates weatherinformation for a given location.
    :param cityname: (str) Name of the city
    :param user_api: (str) API key for openweathermaps.com
    :return: (dict) weather data 
    '''
    complete_api_link = "http://api.weatherinformation.info/current?location="+city_name+"&openweathermaps_api_key="+user_api
    response = requests.get(complete_api_link)
    api_data = response.json()
    return api_data