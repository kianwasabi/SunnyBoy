import requests
from collections import defaultdict

def def_value_dict():
    return "Not Present"

def callOpenWeatherAPI(city_name:str , user_api:str):
    api_data = defaultdict(def_value_dict)
    try: 
        complete_api_link = "https://api.openweathermap.org/data/2.5/weather?q="+city_name+"&appid="+user_api
        response = requests.get(complete_api_link)
        api_data = response.json()
        response.raise_for_status()
        return api_data
    except requests.exceptions.HTTPError as err: 
        print(str(api_data['cod'])+" "+api_data['message'])
        raise SystemExit(err)