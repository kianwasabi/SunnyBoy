import math

class Time(): 
    def __init__(self, timestamp , timezone):
        self.year = timestamp.year
        self.month = timestamp.month
        self.day = timestamp.day
        self.hour = timestamp.hour
        self.minute = timestamp.minute
        self.second = timestamp.second
        self.timezone = timezone
    def getDate(self):
        '''return date at timezone - string'''
        d = "{:02d}".format(self.day)
        m = "{:02d}".format(self.month)
        y = "{:04d}".format(self.year)
        return f"{d}.{m}.{y}"
    def getTime(self):
        '''return time at Timezone - string'''
        h = "{:02d}".format(self.hour)
        m = "{:02d}".format(self.minute)
        s = "{:02d}".format(self.second)
        return f"{h}:{m}:{s}"
    def getTimezone(self):
        '''return Timezone - string'''
        return f"{self.timezone}"
    def _editTimewithTimezone(self):
        self.hour = self.hour + self.timezone

class Location(Time): 
    def __init__(self,name,longitude, latitude, timestamp, timezone):
       Time.__init__(self, timestamp, timezone) 
       self.name = name
       self.longitude = longitude
       self.latitude = latitude
    def getLocationName(self):
        return f"{self.name}"
    def getLongitude(self):
        return f"{self.longitude}"
    def getLatitude(self):
        return f"{self.latitude}"

class Wind(Location):
    def __init__(self, wind_speed, wind_direction, name,longitude, latitude, timestamp, timezone):
        Location.__init__(self, name, longitude, latitude, timestamp, timezone)
        self.speed = wind_speed
        self.direction = wind_direction     
    def getWindSpeed(self):
        return f"{self.speed}"
    def getDirectionDegree(self):
        return f"{self.direction}"
    def getDirectionPoint(self):
        if(self.direction>337.5):
            return 'N'
        if(self.direction>292.5):
            return 'NW'
        if(self.direction>247.5):
            return 'W'
        if(self.direction>202.5):
            return 'SW'
        if(self.direction>157.5):
            return 'S'
        if(self.direction>122.5):
            return 'SE'
        if(self.direction>67.5):
            return 'E'
        if(self.direction>22.5):
            return 'NE'
        return 'N'             

class Weather(Location):
    def __init__(self,temperatur, weather_descr, cloudiness, visibility, name, longitude, latitude, timestamp, timezone):
        Location.__init__(self, name, longitude, latitude, timestamp, timezone)
        self.temperatur = temperatur
        self.weather_descr = weather_descr
        self.cloudiness = cloudiness
        self.visibility = visibility  
    def getTemperatur(self):
        return f"{self.temperatur}"
    def getWeatherDiscription(self):
        return f"{self.weather_descr}"
    def getCloudiness(self):    
        return f"{self.cloudiness}"
    def getVisibility(self):
        return f"{self.visibility}"

class Sun(Location):
    def __init__(self, timestamp_sunrise, timestamp_sunset, name, longitude, latitude, timestamp, timezone):
        Location.__init__(self, name, longitude, latitude, timestamp, timezone)
        self.sunrise = Time(timestamp_sunrise, timezone)
        self.sunset = Time(timestamp_sunset, timezone)
        self.azimuth, self.elevation  = self._SunPosition()
    def getTimeSunrise(self):
        return f"{self.sunrise.getTime()}"
    def getTimeSunset(self):
        return f"{self.sunset.getTime()}"
    def getAzimuth(self):
        return f"{self.azimuth}"
    def getElevation(self):
        return f"{self.elevation}"
    def getSunPosition(self):
        return self.azimuth, self.elevation
    def _SunPosition(self):
        ''' 
        Calculate Azimuth and Elevation
        Source: https://levelup.gitconnected.com/python-sun-position-for-solar-energy-and-research-7a4ead801777
        '''
        refraction = True
        year = self.year
        month = self.month
        day = self.day
        hour = self.hour
        minute = self.minute
        second = self.second
        timezone = self.timezone
        longitude = self.longitude
        latitude = self.latitude 
        #inner function 
        def into_range(x, range_min, range_max):
            shiftedx = x - range_min
            delta = range_max - range_min
            return (((shiftedx % delta) + delta) % delta) + range_min
        rad, deg = math.radians, math.degrees
        sin, cos, tan = math.sin, math.cos, math.tan
        asin, atan2 = math.asin, math.atan2  
        rlat = rad(latitude)
        rlon = rad(longitude) 
        greenwichtime = hour - timezone + minute / 60 + second /3600
        daynum = (
            367 * year
            - 7 * (year + (month + 9) // 12) // 4
            + 275 * month // 9
            + day - 730531.5 + greenwichtime / 24)  
        mean_long = daynum * 0.01720279239 + 4.894967873  
        mean_anom = daynum * 0.01720197034 + 6.240040768  
        eclip_long = (
            mean_long
            + 0.03342305518 * sin(mean_anom)
            + 0.0003490658504 * sin(2 * mean_anom))
        obliquity = 0.4090877234 - 0.000000006981317008 * daynum  
        rasc = atan2(cos(obliquity) * sin(eclip_long), cos(eclip_long))  
        decl = asin(sin(obliquity) * sin(eclip_long))
        sidereal = 4.894961213 + 6.300388099 * daynum + rlon  
        hour_ang = sidereal - rasc  
        elevation = asin(sin(decl) * sin(rlat) + cos(decl) * cos(rlat)* cos(hour_ang))  
        azimuth = atan2(-cos(decl) * cos(rlat) * sin(hour_ang),sin(decl) - sin(rlat) * sin(elevation),)
        azimuth = into_range(deg(azimuth), 0, 360)
        elevation = into_range(deg(elevation), -180, 180)
        if refraction:
            targ = rad((elevation + (10.3 / (elevation + 5.11))))
            elevation += (1.02 / tan(targ)) / 60
        return round(azimuth, 2), round(elevation, 2)
        #self.azimuth = round(azimuth, 2)
        #self.elevation = round(elevation, 2)
        # return f"{self.azimuth} °; {self.elevation} °"
    def getAzimuthPoint(self):
        if(self.azimuth>337.5):
            return 'N'
        if(self.azimuth>292.5):
            return 'NW'
        if(self.azimuth>247.5):
            return 'W'
        if(self.azimuth>202.5):
            return 'SW'
        if(self.azimuth>157.5):
            return 'S'
        if(self.azimuth>122.5):
            return 'SE'
        if(self.azimuth>67.5):
            return 'E'
        if(self.azimuth>22.5):
            return 'NE'
        return 'N'

