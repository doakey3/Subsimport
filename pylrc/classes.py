from .utilities import unpackTimecode, findEvenSplit

class LyricLine():
    """An object that holds a lyric line and it's time"""
    
    def __init__(self, timecode, text=""):
        self.hours = 0
        self.minutes, self.seconds, self.milliseconds = unpackTimecode(timecode)
        self.time = sum([(self.hours * 3600), (self.minutes * 60),
                          self.seconds, (self.milliseconds / 1000)])
        self.text = text
        
    def shift(self, minutes=0, seconds=0, milliseconds=0):
        """Shift the timecode by the given amounts"""
        
        self.addMillis(milliseconds)
        self.addSeconds(seconds)
        self.addMinutes(minutes)
            
    def addMillis(self, milliseconds):
        summation = self.milliseconds + milliseconds
        if summation > 999 or summation < 0:
            self.milliseconds = (self.milliseconds + milliseconds) % 1000
            self.addSeconds(int((self.milliseconds + milliseconds) / 1000))
        else:
            self.milliseconds = summation
    
    def addSeconds(self, seconds):
        summation = self.seconds + seconds
        if summation > 59 or summation < 0:
            self.seconds = (self.seconds + seconds) % 60
            self.addMinutes(int((self.seconds + seconds) / 60))
        else:
            self.seconds = summation
    
    def addMinutes(self, minutes):
        summation = self.minutes + minutes
        if summation > 59 or summation < 0:
            self.minutes = (self.minutes + minutes) % 60
            self.addHours(int((self.minutes + minutes) / 60))
        else:
            self.minutes = self.minutes + minutes
    
    def addHours(self, hours):
        summation = self._hours + hours
        if summation > 23:
            self.hours = 23
        elif summation < 0:
            self.hours = 0
            self.minutes = 0
            self.seconds = 0
            self.milliseconds = 0
        else:
            self._hours = summation

    def __lt__(self, other):
        """For sorting instances of this class"""
        return self.time < other.time

class Lyrics(list):
    """A list that holds the contents of the lrc file"""
    def __init__(self, items=[]):
        
        self.artist = ""
        self.album = ""
        self.title = ""
        self.author = ""
        self.length = ""
        self.offset = ""
        
        self.extend(items)
    
    def toSRT(self):
        """Returns an SRT string of the LRC data"""
        
        if not self[-1].text.rstrip() == "":
            timecode = ''.join(['[', str(self[-1].minutes), ':', 
                                str(self[-1].seconds), '.', 
                                str(self[-1].milliseconds), ']'])
            end_line = LyricLine(timecode, "")
            end_line.shift(seconds=5)
            self.append(end_line)
        
        output = []
        srt = ""
        for i in range(len(self) - 1):
            if not self[i].text == '':
                srt = str(i) + '\n'
                start_hours = "%02d" % self[i].hours
                start_min = "%02d" % self[i].minutes
                start_sec = "%02d" % self[i].seconds
                start_milli = "%03d" % self[i].milliseconds
                start_timecode = ''.join([start_hours, ':', start_min, 
                                          ':', start_sec, ',', start_milli])
                end_hours = "%02d" % self[i + 1].hours
                end_min = "%02d" % self[i + 1].minutes
                end_sec = "%02d" % self[i + 1].seconds
                end_milli = "%03d" % (self[i + 1].milliseconds - 1)
                end_timecode = ''.join([end_hours, ':', end_min, 
                                        ':', end_sec, ',', end_milli])
            
                srt = srt + start_timecode + ' --> ' + end_timecode + '\n'
                if len(self[i].text) > 36:
                    srt = srt + findEvenSplit(self[i].text) + '\n'
                else:
                    srt = srt + self[i].text + '\n'
                output.append(srt)

        return '\n'.join(output).rstrip()
    
    def toLRC(self):
        output = []
        if not self.artist == "":
            output.append('[ar:' + self.artist + ']')
        if not self.album == "":
            output.append('[al:' + self.album + ']')
        if not self.title == "":
            output.append('[ti:' + self.title + ']')
        if not self.author == "":
            output.append('[au:' + self.author + ']')
        if not self.length == "":
            output.append('[length:' + self.length + ']')
        if not self.offset == "":
            output.append('[offset:' + self.offset + ']')
        
        if len(output) > 0:
            output.append('')
        
        lrc = ""
        for i in range(len(self)):
            minutes = "%02d" % self[i].minutes
            seconds = "%02d" % self[i].seconds
            milliseconds = ("%02d" % self[i].milliseconds)[0:2]
            
            lrc = ''.join(['[', minutes, ':', seconds, '.', milliseconds, ']'])
            lrc += self[i].text
            output.append(lrc)
        return '\n'.join(output).rstrip()
        
            
