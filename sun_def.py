from location_def import Location
from time_def import Time
import math

class Sun(Location):
    def __init__(self, timestamp_sunrise, timestamp_sunset, name, longitude, latitude, timestamp, timezone):
        Location.__init__(self, name, longitude, latitude, timestamp, timezone)
        #super().__init__(self,name,longitude, latitude, timestamp, timezone)
        self.sunrise = Time(timestamp_sunrise, timezone)
        self.sunset = Time(timestamp_sunset, timezone)
        self.azimuth, self.elevation  = self.SunPosition()
    def getTimeSunrise(self):
        return self.sunrise.getTime()
    def getTimeSunset(self):
        #self.sunset.editTimewithTimezone()
        return self.sunset.getTime() 
    def getAzimuth(self):
        return f"{self.azimuth} °"
    def getElevation(self):
        return f"{self.elevation} °"
    def getSunPosition(self):
        return self.azimuth, self.elevation
    def SunPosition(self):
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