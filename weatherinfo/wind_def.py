from .location_def import Location

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