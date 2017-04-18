def sec2timecode(sec_time):
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

def text2srt(text):
    """
    Creates an SRT string out of plain text, with 1 second for each 
    segment
    """
    lines = text.split('\n')
    
    output = []
    sec_time = 0
    for i in range(len(lines)):
        seg = str(i) + '\n'
        start = sec2timecode(sec_time)
        sec_time += 0.9
        end = sec2timecode(sec_time) 
        seg += start + ' --> ' + end + '\n'
        
        if len(lines[i].rstrip()) > 36:
            lines[i] = findEvenSplit(lines[i])
        
        seg += lines[i] + '\n'
        output.append(seg)
    
    return '\n'.join(output).rstrip()
