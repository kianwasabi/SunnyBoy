import requests

def callOpenWeatherAPI(city_name:str , user_api:str):
    # def apiLogin (): 
    #     filename = 'OpenWeatherMap.txt'  
    #     try:
    #         with open(filename) as file:
    #             lines = file.readlines()
    #         user_api = lines[-1]
    #         return user_api
    #     except FileNotFoundError as err: 
    #         print(filename,"not found")
    #         raise SystemExit(err)
    #     else: 
    #         return user_api
    # user_api = apiLogin()
    

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