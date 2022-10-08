from datetime import datetime, timezone

class Time(): 
    def __init__(self, timestamp , timezone):
        self.year = timestamp.year #timestamp.strftime("%Y") 
        self.month = timestamp.month #timestamp.strftime("%m")
        self.day = timestamp.day #timestamp.strftime("%d") #
        self.hour = timestamp.hour #timestamp.strftime("%H") #
        self.minute = timestamp.minute #timestamp.strftime("%M") #
        self.second = timestamp.second# timestamp.strftime("%S") #
        # self.year = int(datetime.fromtimestamp(timestamp).strftime("%Y"))
        # self.month = int(datetime.fromtimestamp(timestamp).strftime("%m"))
        # self.day = int(datetime.fromtimestamp(timestamp).strftime("%d"))
        # self.hour = int(datetime.fromtimestamp(timestamp).strftime("%H"))
        # self.minute = int(datetime.fromtimestamp(timestamp).strftime("%M"))
        # self.second = int(datetime.fromtimestamp(timestamp).strftime("%S"))
        self.timezone = timezone
    def getDate(self):
        return f"{self.day}.{self.month}.{self.year}"
    def getTime(self):
        return f"{self.hour}:{self.minute}:{self.minute}"
    def editTimewithTimezone(self):
        self.hour = self.hour + self.timezone