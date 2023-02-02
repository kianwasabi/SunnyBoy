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