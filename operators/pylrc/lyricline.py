from .tools.timecode import unpack_timecode
import re

class LyricLine():
    """An object that holds a lyric line and it's time"""

    def __init__(self, timecode, text=""):
        self.hours = 0
        self.minutes, self.seconds, self.milliseconds = unpack_timecode(timecode)
        self.time = sum([(self.hours * 3600), (self.minutes * 60),
                          self.seconds, (self.milliseconds / 1000)])
        self.text = text

    def shift(self, minutes=0, seconds=0, milliseconds=0):
        """Shift the timecode by the given amounts"""

        self.add_millis(milliseconds)
        self.add_seconds(seconds)
        self.add_minutes(minutes)

    def add_millis(self, milliseconds):
        summation = self.milliseconds + milliseconds
        if summation > 999 or summation < 0:
            self.milliseconds = (self.milliseconds + milliseconds) % 1000
            self.addSeconds(int((self.milliseconds + milliseconds) / 1000))
        else:
            self.milliseconds = summation

    def add_seconds(self, seconds):
        summation = self.seconds + seconds
        if summation > 59 or summation < 0:
            self.seconds = (self.seconds + seconds) % 60
            self.add_minutes(int((self.seconds + seconds) / 60))
        else:
            self.seconds = summation

    def add_minutes(self, minutes):
        summation = self.minutes + minutes
        if summation > 59 or summation < 0:
            self.minutes = (self.minutes + minutes) % 60
            self.add_hours(int((self.minutes + minutes) / 60))
        else:
            self.minutes = self.minutes + minutes

    def add_hours(self, hours):
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

    @property
    def text_without_tags(self):
        re_tag = re.compile(r'<[^>]*?>')
        return re_tag.sub('', self.text)

    @property
    def srt_time(self):
        hours = "%02d" % self.hours
        mins = "%02d" % self.minutes
        secs = "%02d" % self.seconds
        millis = "%03d" % self.milliseconds
        timecode = ''.join([
            hours, ':', mins, ':', secs, ',', millis])
        return timecode

    @property
    def lrc_time(self):
        mins = "%02d" % self.minutes
        secs = "%02d" % self.seconds
        millis = ("%03d" % self.milliseconds)[0:2]

        timecode = ''.join([
            '[', mins, ':', secs, '.', millis, ']'])
        return timecode