from datetime import datetime
import math

def is_timecode(timecode):
    """Checks if a string is a proper lrc timecode"""

    timecode = timecode.replace('<', '[').replace('>', ']')
    try:
        x = datetime.strptime(timecode, '[%M:%S.%f]')
        return True

    except ValueError:
        return False


def timecode_to_seconds(timecode):
    """convert timecode to seconds"""
    timecode = timecode.replace('<', '[').replace('>', ']')
    mins, secs, millis = unpack_timecode(timecode)
    seconds = (mins * 60) + secs + (millis / 1000)
    return seconds


def unpack_timecode(timecode):
    """unpacks a timecode to minutes, seconds, and milliseconds"""
    timecode = timecode.replace('<', '[').replace('>', ']')
    x = datetime.strptime(timecode, '[%M:%S.%f]')

    minutes = x.minute
    seconds = x.second
    milliseconds = int(x.microsecond / 1000)
    return minutes, seconds, milliseconds


def seconds_to_timecode(sec, sym='[]'):
    """Makes a timecode of the format [MM:SS.ff], or <MM:SS.ff>"""

    minutes = "%02d" % int(sec / 60)
    seconds = "%02d" % int(sec % 60)
    millis = ("%03d" % ((sec % 1) * 1000))[0:2]

    if sym == '[]':
        return ''.join(['[', minutes, ':', seconds, '.', millis, ']'])

    elif sym == '<>':
        return ''.join(['<', minutes, ':', seconds, '.', millis, '>'])

def timecode_to_srt(timecode):
    """convert timecode of format [MM:SS.ff] to an srt format timecode"""
    secs = timecode_to_seconds(timecode)

    hours = "00"
    minutes = "%02d" % int(secs / 60)
    seconds = "%02d" % int(secs % 60)
    millis = "%03d" % (round(secs - int(secs), 2) * 1000)

    return ''.join([hours, ':', minutes, ':', seconds, ',', millis])

if __name__ == '__main__':
    print(is_timecode('[05:40.99]'))
    print(timecode_to_seconds('<01:00.99>'))
    print(unpack_timecode('<01:00.99>'))
    print(seconds_to_timecode(200.800, '<>'))
    print(timecode_to_srt('<03:59.29>'))