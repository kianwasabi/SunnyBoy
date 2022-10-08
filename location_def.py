from time_def import Time

class Location(Time): 
    def __init__(self,name,longitude, latitude, timestamp, timezone):
       Time.__init__(self, timestamp, timezone) 
       #super().__init__(self, timestamp, timezone)
       self.name = name
       self.longitude = longitude
       self.latitude = latitude
    def getLocationName(self):
        return f"{self.name}"
    def getLongitude(self):
        return self.longitude
    def getLatitude(self):
        return self.latitude