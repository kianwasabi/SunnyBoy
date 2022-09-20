# --- Include Libraries ---
import requests
import os
import PySimpleGUI as sg
from datetime import datetime, timezone
import os.path
import math

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

class Time(): 
    def __init__(self, timestamp , timezone):
        self.year = datetime.fromtimestamp(timestamp).strftime("Y")
        self.month = datetime.fromtimestamp(timestamp).strftime("m")
        self.day = datetime.fromtimestamp(timestamp).strftime("d")
        self.hours = datetime.fromtimestamp(timestamp).strftime("H")
        self.minute = datetime.fromtimestamp(timestamp).strftime("M")
        self.second = datetime.fromtimestamp(timestamp).strftime("S")
        self.timezone = timezone
    def getDate(self):
        return "{0:02d}:{1:02d}:{2:02d}".format(self.day, self.month,self.year) 
    def getTime(self):
        return "{0:02d}:{1:02d}:{2:02d}".format(self.hours, self.minutes,self.seconds)

class Time(): 
    def __init__(self, timestamp , timezone):
        self.year = 1
        test = datetime.fromtimestamp(timestamp).strftime("Y")
        self.month = datetime.fromtimestamp(timestamp).strftime("m")
        self.day = datetime.fromtimestamp(timestamp).strftime("d")
        self.hour = datetime.fromtimestamp(timestamp).strftime("H")
        self.minute = datetime.fromtimestamp(timestamp).strftime("M")
        self.second = datetime.fromtimestamp(timestamp).strftime("S")
        self.timezone = timezone

def main(): 
    cityname = input("Enter city name: ")
    api_data = callOpenWeatherAPI(cityname)
    time_api_data_calculation = datetime.fromtimestamp(api_data['dt'])
    print (time_api_data_calculation.strftime("%H"))
    t = Time(api_data['dt'],api_data['timezone']/60/60)
    print (t.hour)
    

if __name__ == '__main__':
    main()