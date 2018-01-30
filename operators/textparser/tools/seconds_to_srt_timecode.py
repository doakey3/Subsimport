def seconds_to_srt_timecode(sec_time):
    """
    Converts time (in seconds) into a timecode with the format
    23:59:59,999
    """
    hours = int(sec_time / 3600)
    minutes = int((sec_time % 3600) / 60)
    seconds = int((((sec_time % 3600) / 60) - minutes) * 60)
    milliseconds = int((sec_time - int(sec_time)) * 1000)

    hours = "%02d" % hours
    minutes = "%02d" % minutes
    seconds = "%02d" % seconds
    milliseconds = "%03d" % milliseconds

    return ''.join([hours, ':', minutes, ':', seconds, ',',
                    milliseconds])