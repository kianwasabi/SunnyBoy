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
        return f"{self.day}.{self.month}.{self.year}"
    def getTime(self):
        '''return time at Timezone - string'''
        return f"{self.hour}:{self.minute}:{self.minute}"
    def getTimezone(self):
        '''return Timezone - string'''
        return f"{self.timezone}"
    def _editTimewithTimezone(self):
        self.hour = self.hour + self.timezone