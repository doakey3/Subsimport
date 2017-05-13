from datetime import datetime

def validateTimecode(timecode):
    """Checks if a string is a timecode of format [%M:%S.%f]"""
    
    try:
        x = datetime.strptime(timecode, '[%M:%S.%f]')
        return True
    
    except ValueError:
        return False

def unpackTimecode(timecode):
    """unpacks a timecode to minutes, seconds, and milliseconds"""
    
    x = datetime.strptime(timecode, '[%M:%S.%f]')
    minutes = x.minute
    seconds = x.second
    milliseconds = int(x.microsecond / 1000)
    return minutes, seconds, milliseconds


def findEvenSplit(line):
    """
    Given a string, splits it into two evenly spaced lines
    """
    word_list = line.split(' ')
    differences = []
    for i in range(len(word_list)):
        group1 = ' '.join(word_list[0:i + 1])
        group2 = ' '.join(word_list[i + 1::])
        differences.append(abs(len(group1) - len(group2)))
    index = differences.index(min(differences))
    for i in range(len(word_list)):
        if i == index:
            group1 = ' '.join(word_list[0:i+1])
            group2 = ' '.join(word_list[i+1::])
    
    return ''.join([group1, '\n', group2]).rstrip()
