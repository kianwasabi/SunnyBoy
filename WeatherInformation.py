import requests
import os
import PySimpleGUI as sg
from datetime import datetime, timezone
import os.path
import math

#clear interpreter console
os.system('cls' if os.name == 'nt' else 'clear')

#Class City, Sub & Wind
class City:
    def __init__(self):
        self.name = None
        self.temperatur = None
        self.timezone = None
        self.time_api_data_calculation = None
        self.weather_description = None
        self.longitute = None
        self.latitude = None
class Sun:
    def __init__(self):
        self.cloudiness = None
        self.visibility = None
        self.rise = None
        self.set = None
        self.azimuth = None
        self.azimuth_point = None
        self.elevation = None
class Wind:
    def __init__(self):
        self.speed = None
        self.direction = None
        self.direction_point = None

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

#Convert Degree to Point, North=0°
def  convertDegreetoPoint(degree):
    if(degree>337.5):
        return 'N'
    if(degree>292.5):
        return 'NW'
    if(degree>247.5):
        return 'W'
    if(degree>202.5):
        return 'SW'
    if(degree>157.5):
        return 'S'
    if(degree>122.5):
        return 'SE'
    if(degree>67.5):
        return 'E'
    if(degree>22.5):
        return 'NE'
    return 'N' 

# Get the Sun's apparent location in the sky
def sunpos(when,tz,location,refraction):
    # inner function into_range 
    def into_range(x, range_min, range_max):
        shiftedx = x - range_min
        delta = range_max - range_min
        # Close Encounters latitude, longitude
        return (((shiftedx % delta) + delta) % delta) + range_min
    #Extract the passed data
    year = when.year
    month = when.month
    day = when.day
    hour = when.hour
    minute = when.minute
    second = when.second
    timezone = tz
    longitude, latitude = location  
    #Math typing shortcuts
    rad, deg = math.radians, math.degrees
    sin, cos, tan = math.sin, math.cos, math.tan
    asin, atan2 = math.asin, math.atan2  
    # Convert latitude and longitude to radians
    rlat = rad(latitude)
    rlon = rad(longitude) 
    # Decimal hour of the day at Greenwich
    greenwichtime = hour - timezone + minute / 60 + second /3600  # Days from J2000, accurate from 1901 to 2099
    daynum = (
        367 * year
        - 7 * (year + (month + 9) // 12) // 4
        + 275 * month // 9
        + day
        - 730531.5
        + greenwichtime / 24
        )  
    # Mean longitude of the sun
    mean_long = daynum * 0.01720279239 + 4.894967873  
    # Mean anomaly of the Sun
    mean_anom = daynum * 0.01720197034 + 6.240040768  
    # Ecliptic longitude of the sun
    eclip_long = (
        mean_long
        + 0.03342305518 * sin(mean_anom)
        + 0.0003490658504 * sin(2 * mean_anom)
        )
    # Obliquity of the ecliptic
    obliquity = 0.4090877234 - 0.000000006981317008 * daynum  
    # Right ascension of the sun
    rasc = atan2(cos(obliquity) * sin(eclip_long), cos(eclip_long))  
    # Declination of the sun
    decl = asin(sin(obliquity) * sin(eclip_long))  
    # Local sidereal time
    sidereal = 4.894961213 + 6.300388099 * daynum + rlon  
    # Hour angle of the sun
    hour_ang = sidereal - rasc  
    # Local elevation of the sun
    elevation = asin(sin(decl) * sin(rlat) + cos(decl) * cos(rlat)* cos(hour_ang))  
    # Local azimuth of the sun
    azimuth = atan2(-cos(decl) * cos(rlat) * sin(hour_ang),sin(decl) - sin(rlat) * sin(elevation),)
    # Convert azimuth and elevation to degrees
    azimuth = into_range(deg(azimuth), 0, 360)
    elevation = into_range(deg(elevation), -180, 180)
    # Refraction correction (optional)
    if refraction:
        targ = rad((elevation + (10.3 / (elevation + 5.11))))
        # Return azimuth and elevation in degrees
        elevation += (1.02 / tan(targ)) / 60
        return (round(azimuth, 2)), round(elevation, 2)

def printinTerminal(city1,wind1,sun1):
    print ("-------------------------------------------------------------")
    print ("Location             :",format(city1.name.upper()))
    print ("Longitude            :",city1.latitude)
    print ("Latitude             :",city1.longitute)
    print ("Temperature          : {:.2f} °C".format(city1.temperatur))
    print ("Weather Description  :",city1.weather_description)
    print ("Calc. Time  API-Data :",city1.time_api_data_calculation.strftime("%Y-%m-%d | %H:%M:%S"))
    print ("-------------------------------------------------------------")
    print ("Cloudiness           :",sun1.cloudiness,"%")
    print ("Visibility           :",sun1.visibility,"m")
    print ("Sun Azimuth          :",sun1.azimuth,"°","(",sun1.azimuth_point,")")
    print ("Sun Elevation        :",sun1.elevation,"°")
    print ("Sunrise              :",sun1.rise,"+",city1.timezone,"h (UTC)")
    print ("Sunset               :",sun1.set,"+",city1.timezone,"h (UTC)")
    print ("-------------------------------------------------------------")
    print ("Wind Speed           :",wind1.speed,"km/h")
    print ("Wind Direction       :",wind1.direction,"°","(",wind1.direction_point,")")

def main(): 
    #init city, wind and sun object
    city1 = City()
    wind1 = Wind()
    sun1 = Sun()
    #Get User Location 
    city1.name = input("Enter city name: ")
    #Get Weather Information from OpenWeatherMap.org/api
    api_data = callOpenWeatherAPI(city1.name)
    #Assign general weather Informations for the choosen location
    city1.longitute = api_data['coord']['lat']
    city1.latitude = api_data['coord']['lon']
    city1.temperatur = ((api_data['main']['temp']) - 273.15) #°F to °C
    city1.timezone = api_data['timezone']/60/60 #Shift in seconds from UTC 
    city1.time_api_data_calculation = datetime.fromtimestamp(api_data['dt'])
    city1.weather_description = api_data['weather'][0]['description']
    #Assign Informations about the sun
    sun1.rise = datetime.utcfromtimestamp(api_data['sys']['sunrise']).strftime("%H:%M:%S")
    sun1.set = datetime.utcfromtimestamp(api_data['sys']['sunset']).strftime("%H:%M:%S") 
    sun1.cloudiness = api_data['clouds']['all']
    sun1.visibility = api_data['visibility']  
    sun1.azimuth, sun1.elevation = sunpos(city1.time_api_data_calculation, city1.timezone, 
                                        (city1.latitude, city1.longitute), True)
    sun1.azimuth_point = convertDegreetoPoint(sun1.azimuth)
    #Assign Informations about the wind
    wind1.speed = api_data['wind']['speed']
    wind1.direction = api_data['wind']['deg']
    wind1.direction_point = convertDegreetoPoint(wind1.direction)
    #Print all in Terminal
    printinTerminal(city1,wind1,sun1)

if __name__ == '__main__':
    main()