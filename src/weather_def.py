from src.location_def import Location

class Weather(Location):
    def __init__(self,temperatur, weather_descr, cloudiness, visibility, name, longitude, latitude, timestamp, timezone):
        Location.__init__(self, name, longitude, latitude, timestamp, timezone)
        #super().__init__(self, name,longitude, latitude, timestamp, timezone)
        self.temperatur = temperatur
        self.weather_descr = weather_descr
        self.cloudiness = cloudiness
        self.visibility = visibility
    def getTemperatur(self):
        return f"{self.temperatur} °C"
    def getWeatherDiscription(self):
        return f"{self.weather_descr}"